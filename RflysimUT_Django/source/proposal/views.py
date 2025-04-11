from django.shortcuts import render
from rest_framework import viewsets
from source.proposal.models import Modes, Proposals, ProposalTypes
from source.proposal.serializers import (
    ModesSerializer,
    ProposalsSerializer,
    ProposalTypesSerializer,
)
# Create your views here.

class ModesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Modes.objects.all()
    serializer_class = ModesSerializer

class ProposalTypesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ProposalTypes.objects.all()
    serializer_class = ProposalTypesSerializer

class ProposalsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Proposals.objects.all()
    serializer_class = ProposalsSerializer