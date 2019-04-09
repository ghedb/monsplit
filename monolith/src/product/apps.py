from django.apps import AppConfig


class ProductAppConfig(AppConfig):
    name = 'product'

    def ready(self):
        import product.signals
