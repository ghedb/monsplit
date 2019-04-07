from django.db import transaction
from django.urls import reverse

from catalog.const import CatalogEventTypes
from catalog.models import Event
from catalog.tasks import submit_event


def catalog_created(catalog_obj):
    return __create_event(catalog_obj, CatalogEventTypes.CREATED)


def catalog_updated(catalog_obj):
    return __create_event(catalog_obj, CatalogEventTypes.UPDATED)


def __create_event(catalog_obj, event_type):
    event_object = Event.objects.create(
        content_object=catalog_obj,
        body={}
    )
    event_object.body = event_serializer(
        catalog_obj,
        event_type,
        event_object.id,
        event_object.time_created
    )
    event_object.save()
    # Publish event on db commit
    transaction.on_commit(
        lambda: submit_event.delay(event_object.id)
    )
    return event_object


def event_serializer(catalog_obj, event_type, event_id, event_date):
    api_endpoint = reverse(
        'api:catalog-detail',
        kwargs={'pk': catalog_obj.pk}
    )

    body = {
        'version': '1',
        'catalogId': catalog_obj.id,
        'eventId': event_id,
        'name': event_type,
        'api': api_endpoint,
        'dateOccurred': event_date.isoformat(),
        'data': {
            'productName': catalog_obj.product.name,
            'productUUID': catalog_obj.product.product_uuid,
            'market': catalog_obj.market.name,
            'marketISOCode': catalog_obj.market.iso_code,
            'StartOffering': catalog_obj.availability_date,
            'OfferingEnds': catalog_obj.availability_end_date,
        }
    }
    # event type specific message changes here
    return body
