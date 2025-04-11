from rest_framework import serializers

from source.evaluation.models import Index,Values
from rest_framework.filters import BaseFilterBackend


class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Index
        fields = '__all__'


class ValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Values
        fields = '__all__'