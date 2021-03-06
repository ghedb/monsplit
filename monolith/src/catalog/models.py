import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_extensions.db.fields.json import JSONField


class Event(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        related_name='catalog_events'
    )
    object_id = models.CharField(max_length=50)
    time_created = models.DateTimeField(auto_now_add=True)
    content_object = GenericForeignKey(
        'content_type',
        'object_id'
    )
    body = JSONField()
    sent = models.BooleanField(
        default=False
    )

    def __str__(self):
        return '{0} {1}'.format(self.body.get('name', ''), self.content_object)

    class Meta:
        ordering = ['-time_created']


class Market(models.Model):
    iso_code = models.CharField(
        max_length=2,
        verbose_name='ISO Code',
        default='',
        blank=True,
    )

    name = models.CharField(
        max_length=40,
        verbose_name='Market Name',
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = (
            'name',
        )


class CatalogEntry(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    product = models.ForeignKey(
        'product.Product',
        related_name='catalog_entries',
        on_delete=models.CASCADE
    )
    market = models.ForeignKey(
        Market,
        related_name='catalog_entries',
        verbose_name='Market',
        on_delete=models.CASCADE
    )
    availability_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Product offering start',
        db_index=True,
    )

    availability_end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Product offering ends',
        db_index=True
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At',
        null=True,
    )

    def __str__(self):
        return 'Catalog Entry: {}, {}, {}'.format(
            self.product.name,
            self.market.name,
            self.availability_date
        )

