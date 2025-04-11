from django.urls import include, path
from rest_framework import routers

from source.evaluation import views

router = routers.DefaultRouter()
router.register(r'index', views.IndexViewSet)
router.register(r'values', views.ValuesViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
