from django.shortcuts import render
from rest_framework import viewsets

from source.air_road.models import Permissions, Layers, Nodes, Edges, Airports
from source.air_road.serializers import PermissionsSerializer, LayersSerializer, NodesSerializer, EdgesSerializer, AirportsSerializer


class PermissionsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Permissions.objects.all()
    serializer_class = PermissionsSerializer

class LayersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Layers.objects.all()
    serializer_class = LayersSerializer

class NodesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Nodes.objects.all()
    serializer_class = NodesSerializer


class EdgesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Edges.objects.all()
    serializer_class = EdgesSerializer


class AirportsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Airports.objects.all()
    serializer_class = AirportsSerializer
