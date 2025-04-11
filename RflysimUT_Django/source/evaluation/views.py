from django.shortcuts import render
from rest_framework import viewsets
from source.evaluation.models import Index, Values
from source.evaluation.serializers import IndexSerializer, ValuesSerializer


class IndexViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Index.objects.all()
    serializer_class = IndexSerializer


class ValuesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Values.objects.all()
    serializer_class = ValuesSerializer