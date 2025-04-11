from django.urls import include, path
from rest_framework import routers

from source.flight_plan import views

router = routers.DefaultRouter()
router.register(r'flight_requirements', views.FlightRequirementsViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
