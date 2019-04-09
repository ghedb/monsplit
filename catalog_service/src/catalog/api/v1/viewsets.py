from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from catalog.api.v1.serializers import (
    CatalogSerializer,
    CatalogUpdateSerializer,
    CatalogCreateSerializer
)
from catalog.models import CatalogEntry

from catalog import service


# Using model viewset to shortcut
# Real advantage would come from using more generic and tying it into the
# service and events
class CatalogViewset(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):
    model = CatalogEntry
    serializer_class = CatalogSerializer
    queryset = CatalogEntry.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = CatalogCreateSerializer(data=request.data, partial=True)
        # TODO add real validation
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        cat_obj = service.create_catalog_entry(
            product_uuid=data.get('product'),
            market_iso_code=data.get('market'),
            start_date=data.get('availability_date'),
            end_date=data.get('availability_end_date')
        )
        serializer = CatalogSerializer(instance=cat_obj)
        return Response(serializer.data)


class CatalogUpdateViewSet(APIView):

    def put(self, request, *args, **kwargs):
        catalog_id = kwargs.get('catalog_id')
        cat_obj = get_object_or_404(CatalogEntry, id=catalog_id)
        serializer = CatalogUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        start_date = data.get('availability_date')
        end_date = data.get('availability_end_date')
        cat_obj = service.update_catalog_entry(
            cat_obj=cat_obj,
            start_date=start_date,
            end_date=end_date,
        )
        serializer = CatalogSerializer(instance=cat_obj)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        catalog_id = kwargs.get('catalog_id')
        cat_obj = get_object_or_404(CatalogEntry, id=catalog_id)
        serializer = CatalogSerializer(instance=cat_obj)
        return Response(serializer.data)
