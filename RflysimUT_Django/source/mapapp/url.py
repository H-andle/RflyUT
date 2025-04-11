from .views import (ClickAirportAPIView, ClickNodeAPIView,DeleteAirportAPIView,
                    ClickEdgeAPIView, DeleteNodeAPIView, DeleteEdgeAPIView, DeleteAllAPIView)
from django.urls import path
from .views import map_view

urlpatterns = [
    path('maps/', map_view, name='mapapp-html'),
    path('maps/add_airport/', ClickAirportAPIView.as_view(), name='mapapp-html'),
    path('maps/add_node/', ClickNodeAPIView.as_view(), name='mapapp-html'),
    path('maps/add_edge/', ClickEdgeAPIView.as_view(), name='mapapp-html'),
    path('maps/delete_airport/', DeleteAirportAPIView.as_view(), name='mapapp-html'),
    path('maps/delete_node/', DeleteNodeAPIView.as_view(), name='mapapp-html'),
    path('maps/delete_edge/', DeleteEdgeAPIView.as_view(), name='mapapp-html'),
    path('maps/delete_all/', DeleteAllAPIView.as_view(), name='mapapp-html')
]

