from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from catalog.api.v1.serializers import (
    CatalogSerializer,
    CatalogUpdateSerializer
)
from catalog.models import CatalogEntry

from catalog import service


class CatalogViewset(ModelViewSet):
    model = CatalogEntry
    serializer_class = CatalogSerializer
    queryset = CatalogEntry.objects.all()



class CatalogUpdateViewSet(APIView):

    def put(self, request, *args, **kwargs):
        catalog_id = kwargs.get('catalog_id')
        cat_obj = get_object_or_404(CatalogEntry, id=catalog_id)
        serializer = CatalogUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        import pprint
        pprint.pprint(data)
        start_date = data.get('availability_date')
        end_date = data.get('availability_end_date')
        pprint.pprint(start_date)
        pprint.pprint(end_date)
        cat_obj = service.update_catalog_entry(
            cat_obj,
            start_date=start_date,
            end_date=end_date,
        )
        serializer = CatalogSerializer(instance=cat_obj)
        return Response(serializer.data)




'''

{
"availability_date": "2019-04-05", 
"availability_end_date": null
}

'''