import json
import logging
import os
import sys
import time
from pprint import pprint

import django

from catalog.const import ProductEventTypes, CONSUMER_GROUP

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "catalog_service.settings")
django.setup()

from dateutil.parser import parse
from catalog.models import Product
from django.db.transaction import atomic
from pykafka import KafkaClient
from pykafka.exceptions import NoBrokersAvailableError, SocketDisconnectedError


KAFKA_HOSTS = 'localhost:9092'
ZOOKEEPER_HOSTS = 'localhost:2181'


PRODUCT_TOPIC = 'product'
CATALOG_TOPIC = 'catalog'

class EventProcessingFailure(Exception):
    pass


def create_consumer(topic_name):

    hosts = KAFKA_HOSTS
    zookeeper_host = ZOOKEEPER_HOSTS
    kafka_client = KafkaClient(hosts=hosts)
    topic = kafka_client.topics[topic_name]
    consumer = topic.get_balanced_consumer(
        consumer_group=CONSUMER_GROUP,
        auto_commit_enable=False,
        zookeeper_hosts=zookeeper_host
    )
    return consumer


def event_handler(message):
    try:
        if message.value:
            message = json.loads(message.value.decode('utf-8'))
        else:
            message = {'name': 'empty'}

        event_type = message['name']
        # As of now only create and update events are generated so
        # no change in behaviour, based on the type.

        product_updates = [
            ProductEventTypes.CREATED,
            ProductEventTypes.UPDATED,

        ]
        if event_type in product_updates:
            update_product(message)

        elif event_type == ProductEventTypes.DISCONTINUED:
            product_discontinued(message)

    except Exception as err:
        raise EventProcessingFailure(err)


def is_new_event(object_updated_at, date_occurred):
    if object_updated_at:
        return object_updated_at < date_occurred
    else:
        # No updated at set, assume event is newer.
        return True


@atomic()
def update_product(event_dict):
    pprint(event_dict)
    event_data = event_dict['data']
    date_occurred = parse(event_dict['dateOccurred'])

    product_obj, created = Product.objects.get_or_create(
        product_uuid=event_data['productUUID']
    )

    if not created and not is_new_event(product_obj.updated_at, date_occurred):
        # Event date is older than object update date
        # Since all events are currently "update"
        # we do not update with "older" data
        return

    product_obj.name = event_data['productName']
    product_obj.product_category = event_data['productCategory']
    # Discontinued updated here until monolith service can send "discontinued" events
    product_obj.discontinued = event_data['discontinued']
    product_obj.updated_at = date_occurred
    product_obj.save()


@atomic()
def product_discontinued(event_dict):
    event_data = event_dict['data']
    date_occurred = parse(event_dict['dateOccurred'])

    product_obj, created = Product.objects.get_or_create(
        product_uuid=event_data['productUUID']
    )

    if not created and not is_new_event(product_obj.updated_at, date_occurred):
        # Event date is older than object update date
        # Since all events are currently "update"
        # we do not update with "older" data
        return

    product_obj.discontinued = event_data['discontinued']
    product_obj.updated_at = date_occurred
    product_obj.save()


def start_consume(topics):

    log = logging.getLogger()
    consumers = []
    for topic in topics:
        consumers.append(create_consumer(topic))
    while True:
        for consumer in consumers:
            try:
                message = consumer.consume(block=False)
                if message is not None:
                    event_handler(message)
                    consumer.commit_offsets()
            except (SocketDisconnectedError, NoBrokersAvailableError) as err:
                log.error(
                    'Caught Exception {0}\n restarting consumer'.format(
                        err
                    )
                )
                consumer.stop()
                consumer.start()
            except EventProcessingFailure as err:
                log.error(
                    'Caught Exception {0}\n Stopping all consumers'.format(
                        err
                    )
                )
                for consumer in consumers:
                    consumer.stop()
                    raise

            except Exception as err:
                log.error(
                    'Caught unhandled exception {0}\n'.format(
                        err
                    )
                )
                for consumer in consumers:
                    consumer.stop()
                raise Exception(err)
            time.sleep(0.1)


if __name__ == "__main__":
    root = logging.getLogger(__name__)
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    try:
        topics = [PRODUCT_TOPIC, CATALOG_TOPIC]
        start_consume(topics)
    except Exception as err:
        # delay to prevent container
        # from spinning up/down too fast in case of failure
        root.error(err)
        time.sleep(20)
        sys.exit(1)
