from rest_framework import routers

from catalog.api.v1.viewsets import CatalogViewset

urlpatterns = []
router = routers.SimpleRouter()
router.register(
    r'',
    CatalogViewset,
    base_name='catalog'
)

urlpatterns += router.urls