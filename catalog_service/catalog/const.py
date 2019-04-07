class CatalogEventTypes(str):
    CREATED = 'CATALOG_ENTRY_CREATED'
    UPDATED = 'CATALOG_ENTRY_UPDATED'


class ProductEventTypes(str):
    CREATED = 'PRODUCT_CREATED'
    UPDATED = 'PRODUCT_UPDATED'
    DISCONTINUED = 'PRODUCT_DISCONTINUED'


CATALOG_TOPIC = 'catalog'
CONSUMER_GROUP = 'roadmap'