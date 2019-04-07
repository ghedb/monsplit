import json
import logging
import os
import sys
import time
from pprint import pprint

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monolith.settings")
django.setup()

from catalog.const import CatalogEventTypes, CATALOG_TOPIC
from catalog.models import CatalogEntry, Market
from product.models import Product
from dateutil.parser import parse
from django.db.transaction import atomic
from pykafka import KafkaClient
from pykafka.exceptions import NoBrokersAvailableError, SocketDisconnectedError


KAFKA_HOSTS = 'localhost:9092'
ZOOKEEPER_HOSTS = 'localhost:2181'

CONSUMER_GROUP = 'monolith'


class EventProcessingFailure(Exception):
    pass


def create_consumer(topic_name):
    """
    Connect to the Kafka endpoint and start consuming
    messages from the given `topic`.

    The given callback is applied on each
    message.
    """
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
        catalog_events_to_process = [
            CatalogEventTypes.CREATED,
            CatalogEventTypes.UPDATED
        ]
        if event_type in catalog_events_to_process:
            process_catalog_event(message)
    except Exception as err:
        raise EventProcessingFailure(err)


def is_new_event(object_updated_at, date_occurred):
    if object_updated_at:
        return object_updated_at < date_occurred
    else:
        # No updated_at set, assume event is newer.
        return True


@atomic()
def process_catalog_event(event_dict):
    pprint(event_dict)
    event_data = event_dict['data']
    date_occurred = parse(event_dict['dateOccurred'])
    market_obj = Market.objects.get(iso_code=event_data['marketISOCode'])
    product_obj = Product.objects.get(product_uuid=event_data['productUUID'])
    cat_obj, created = CatalogEntry.objects.get_or_create(
        product=product_obj,
        market=market_obj
    )

    if not created and not is_new_event(cat_obj.updated_at, date_occurred):
        # Event date is older than object update date
        # Since all events are currently "update"
        # we do not update with "older" data
        return

    cat_obj.updated_at = date_occurred
    cat_obj.availability_date = event_data['StartOffering']
    cat_obj.availability_end_date = event_data['OfferingEnds']
    cat_obj.save()


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
        topics = [CATALOG_TOPIC]
        start_consume(topics)
    except Exception as err:
        # delay to prevent container from
        # spinning up/down too fast in case of failure
        root.error(err)
        time.sleep(20)
        sys.exit(1)
