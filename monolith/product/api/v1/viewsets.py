
from rest_framework.viewsets import ModelViewSet

from product.api.v1.serializers import ProductSerializer
from product.models import Product


class ProductViewset(ModelViewSet):
    model = Product
    serializer_class = ProductSerializer
    queryset = Product.objects.all()