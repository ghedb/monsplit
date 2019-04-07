
from django.db import transaction
from django.urls import reverse

from product.const import ProductEventTypes
from product.models import Event
from product.tasks import submit_event


def product_created(product_obj):
    return __create_event(product_obj, ProductEventTypes.CREATED)


def product_updated(product_obj):
    return __create_event(product_obj, ProductEventTypes.UPDATED)


def product_discontinued(product_obj):
    return __create_event(product_obj, ProductEventTypes.DISCONTINUED)


def __create_event(product_obj, event_type):
    event_object = Event.objects.create(
        content_object=product_obj,
        body={}
    )
    event_object.body = event_serializer(
        product_obj,
        event_type,
        event_object.id,
        event_object.time_created
    )
    event_object.save()
    # Publish event on db commit
    print('on commit')
    transaction.on_commit(
        lambda: submit_event.delay(event_object.id)
    )
    return event_object


def event_serializer(product_obj, event_type, event_id, event_date):
    api_endpoint = reverse(
        'v1:product:product-detail',
        kwargs={'pk': product_obj.pk}
    )

    body = {
        'version': '1',
        'productId': product_obj.id,
        'eventId': event_id,
        'name': event_type,
        'api': api_endpoint,
        'dateOccurred': event_date.isoformat(),
        'data': {
            'productName': product_obj.name,
            'productUUID': product_obj.product_uuid,
            'discontinued': product_obj.discontinued,
            'productCategory': product_obj.product_category,
        }
    }
    # event type specific message changes here
    return body
