from django.urls import include, path
from rest_framework import routers

from source.uav import views

router = routers.DefaultRouter()
router.register(r'drone', views.DroneViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('get_drones_state/', views.get_drones_state, name='get_drones_state')
]
