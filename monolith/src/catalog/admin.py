from django.contrib import admin

# Register your models here.
from catalog.models import CatalogEntry, Market

admin.site.register(CatalogEntry, admin.ModelAdmin)
admin.site.register(Market, admin.ModelAdmin)