from celery import shared_task
from celery.utils.log import get_task_logger
from django.db.transaction import atomic

from product.const import PRODUCT_TOPIC
from product.models import Event
from monolith.event_producer import send_event

logger = get_task_logger(__name__)


@shared_task
def submit_event(event_id):
    event = Event.objects.get(id=event_id)
    with atomic():
        send_event(PRODUCT_TOPIC, event.body)
        event.sent = True
        event.save()


@shared_task
def create_events():
    new_events = Event.objects.filter(sent=False)
    for event in new_events:
        try:
            submit_event(event.id)
        except Exception as e:
            logger.error(
                'Sending product events failed due to {0}'.format(e)
            )
            raise e
    return
