from rest_framework import routers
from django.urls import path
from catalog.api.v1.viewsets import CatalogViewset, CatalogUpdateViewSet

urlpatterns = [
   path('<uuid:catalog_id>/', CatalogUpdateViewSet.as_view()),
]
router = routers.SimpleRouter()
router.register(
    r'',
    CatalogViewset,
    base_name='catalog'
)

urlpatterns += router.urls