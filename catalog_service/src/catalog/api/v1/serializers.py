from rest_framework import serializers

from catalog.models import CatalogEntry


class CatalogSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source='product.product_uuid')
    market = serializers.ReadOnlyField(source='market.iso_code')

    class Meta:
        model = CatalogEntry
        fields = '__all__'


class CatalogUpdateSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    product = serializers.ReadOnlyField(source='product.product_uuid')
    market = serializers.ReadOnlyField(source='market.iso_code')
    availability_date = serializers.DateField()
    availability_end_date = serializers.DateField(allow_null=True)


class CatalogCreateSerializer(serializers.Serializer):
    product = serializers.UUIDField()
    market = serializers.CharField()
    availability_date = serializers.DateField()
    availability_end_date = serializers.DateField(allow_null=True)