

from rest_framework.viewsets import ModelViewSet

from catalog.api.v1.serializers import CatalogSerializer
from catalog.models import CatalogEntry


class CatalogViewset(ModelViewSet):
    model = CatalogEntry
    serializer_class = CatalogSerializer
    queryset = CatalogEntry.objects.all()