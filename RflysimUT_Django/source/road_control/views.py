from django.shortcuts import render
from rest_framework import viewsets

from source.road_control.models import RoadControl
from source.road_control.serializers import RoadControlSerializer

class RoadControlViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = RoadControl.objects.all()
    serializer_class = RoadControlSerializer
