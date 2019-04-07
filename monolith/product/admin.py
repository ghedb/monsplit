from django.contrib import admin

# Register your models here.
from product.models import Product, Event

admin.site.register(Product, admin.ModelAdmin)
admin.site.register(Event, admin.ModelAdmin)