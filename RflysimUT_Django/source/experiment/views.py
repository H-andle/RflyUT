from django.shortcuts import render
from rest_framework import viewsets

from source.experiment.models import Experiments, FlightLogs, EdgeLogs
from source.experiment.serializers import ExperimentsSerializer, FlightLogsSerializer, EdgeLogsSerializer

class ExperimentsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Experiments.objects.all()
    serializer_class = ExperimentsSerializer

class FlightLogsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = FlightLogs.objects.all()
    serializer_class = FlightLogsSerializer

class EdgeLogsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = EdgeLogs.objects.all()
    serializer_class = EdgeLogsSerializer