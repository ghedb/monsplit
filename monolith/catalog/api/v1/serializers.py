from rest_framework import serializers

from catalog.models import CatalogEntry


class CatalogSerializer(serializers.ModelSerializer):

    class Meta:
        model = CatalogEntry
        fields = '__all__'