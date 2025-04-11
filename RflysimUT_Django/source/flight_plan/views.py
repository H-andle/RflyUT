from django.shortcuts import render
from rest_framework import viewsets
from source.flight_plan.models import FlightRequirements
from source.flight_plan.serializers import FlightRequirementsSerializer
# Create your views here.

class FlightRequirementsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = FlightRequirements.objects.all()
    serializer_class = FlightRequirementsSerializer