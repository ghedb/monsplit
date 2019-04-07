from django.db.transaction import atomic

from catalog.events import (
    catalog_created,
    catalog_updated
)
from catalog.models import (
    Product,
    CatalogEntry,
    Market
)


@atomic()
def create_catalog_entry(product_uuid, market_iso_code, start_date, end_date):
    product_obj = get_product_by_uuid(product_uuid)
    market_obj = get_market(market_iso_code)


    cat_obj = CatalogEntry.objects.create(
        product=product_obj,
        market=market_obj,
        availability_date=start_date,
        availability_end_date=end_date
    )
    catalog_created(cat_obj)
    return cat_obj


def get_product_by_uuid(product_uuid):
    return Product.objects.get(product_uuid=product_uuid)


def get_product_by_id(product_id):
    return Product.objects.get(id=product_id)


def get_market_by_iso(market_iso_code):
    return Market.objects.get(iso_code=market_iso_code)


@atomic()
def update_catalog_entry(cat_obj, start_date, end_date):
    print(cat_obj.availability_date)
    print(cat_obj.availability_end_date)
    cat_obj.availability_date = start_date
    cat_obj.availability_end_date = end_date
    cat_obj.save()
    catalog_updated(cat_obj)
    return cat_obj

