from django.contrib import admin

# Register your models here.
from catalog.models import (
    CatalogEntry,
    Product,
    Event,
    Market
)

admin.site.register(CatalogEntry, admin.ModelAdmin)
admin.site.register(Product, admin.ModelAdmin)
admin.site.register(Event, admin.ModelAdmin)
admin.site.register(Market, admin.ModelAdmin)