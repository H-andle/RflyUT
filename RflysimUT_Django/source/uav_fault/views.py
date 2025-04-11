from django.shortcuts import render
from rest_framework import viewsets
from source.uav_fault.models import FaultPlans
from source.uav_fault.serializers import FaultPlansSerializer
# Create your views here.

class FaultPlansViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = FaultPlans.objects.all()
    serializer_class = FaultPlansSerializer