import uuid

from django.contrib.contenttypes.fields import GenericForeignKey, ContentType
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

# Create your models here.
from django_extensions.db.fields.json import JSONField


class ProductuerySet(models.QuerySet):
    def all(self):
        return self.filter(discontinued=False)


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Product Name'
    )
    product_uuid = models.UUIDField(
        default=uuid.uuid4,
        verbose_name='Unique ID for product',
        help_text='Unique identifier for product across services',
        unique=True
    )

    product_category = models.CharField(
        max_length=25,
    )
    discontinued = models.BooleanField(default=False)

    objects = ProductuerySet.as_manager()

    def __str__(self):
        return '{0} - {1}'.format(self.name, self.product_uuid)

    class Meta:
        unique_together = ('name', 'product_category')


class Event(models.Model):
    """Event table that stores all model changes"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        verbose_name='Unique ID for Event',
        editable=False
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        related_name='product_events'
    )
    object_id = models.CharField(max_length=50)
    time_created = models.DateTimeField(auto_now_add=True)
    content_object = GenericForeignKey(
        'content_type',
        'object_id',
    )
    body = JSONField()
    sent = models.BooleanField(
        default=False
    )

    def __str__(self):
        return '{0} {1}'.format(self.body.get('name', ''), self.content_object)