import json

from pykafka import KafkaClient

kafka_client = None
producers = {}


KAFKA_HOST = 'localhost:9092'
ZOOKEEPER_HOST = 'localhost:2181'


def start_events_producer(topic):
    """
    Start an event producer in the background.
    """

    topic_name = topic
    hosts = KAFKA_HOST
    kafka_client = KafkaClient(hosts=hosts)
    topic = kafka_client.topics[topic]
    producers[topic_name] = topic.get_producer()


def send_event(topic, event):
    """
    Push event to the given topic.
    Create producer for topic if one does not already exist
    """
    assert isinstance(event, dict)

    if topic not in producers:
        start_events_producer(topic=topic)
    event = json.dumps(event).encode('utf-8')

    producer = producers[topic]
    producer.produce(event,)
