from django.db.models.signals import post_save
from django.dispatch import receiver

from product.events import product_updated


@receiver(post_save, sender='product.Product')
def product_saved(sender, instance, created, **kwargs):
    product_updated(instance)