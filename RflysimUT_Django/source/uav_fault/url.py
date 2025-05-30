from django.urls import include, path
from rest_framework import routers

from source.uav_fault import views

router = routers.DefaultRouter()
router.register(r'fault_plans', views.FaultPlansViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
