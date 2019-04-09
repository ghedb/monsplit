# -*- coding: utf-8 -*-
import json
from django.conf import settings

from pykafka import KafkaClient

producers = {}


def start_events_producer(topic):
    """
    Start an event producer in the background.
    """

    topic_name = topic
    kafka_client = KafkaClient(hosts=settings.KAFKA_HOSTS)
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
    producer.produce(event)
