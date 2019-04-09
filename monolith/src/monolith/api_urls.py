from django.urls import path, include


urlpatterns = [
    path(
        'catalog',
        include(
            ('catalog.api.v1.api_urls', 'catalog'),
            namespace='catalog')
    ),
    path(
        'product',
        include(
            ('product.api.v1.api_urls', 'product'),
            namespace='product')
    ),
]