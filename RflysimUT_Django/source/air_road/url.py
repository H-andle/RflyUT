from django.urls import include, path
from rest_framework import routers

from source.air_road import views

router = routers.DefaultRouter()
router.register(r'permissions', views.PermissionsViewSet)
router.register(r'layers', views.LayersViewSet)
router.register(r'nodes', views.NodesViewSet)
router.register(r'edges', views.EdgesViewSet)
router.register(r'airports', views.AirportsViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
