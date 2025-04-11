from django.urls import include, path
from rest_framework import routers

from source.proposal import views

router = routers.DefaultRouter()
router.register(r'proposals', views.ProposalsViewSet)
router.register(r'proposal_types', views.ProposalTypesViewSet)
router.register(r'modes', views.ModesViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
