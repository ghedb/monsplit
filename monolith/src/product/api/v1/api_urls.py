from rest_framework import routers

from product.api.v1.viewsets import ProductViewset

urlpatterns = []
router = routers.SimpleRouter()
router.register(
    r'',
    ProductViewset,
    base_name='product'
)

urlpatterns += router.urls