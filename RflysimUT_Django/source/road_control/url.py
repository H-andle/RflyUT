from django.urls import include, path
from rest_framework import routers

from source.road_control import views

router = routers.DefaultRouter()
router.register(r'road_control', views.RoadControlViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
