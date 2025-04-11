from rest_framework import serializers

from source.uav_fault.models import FaultPlans
from rest_framework.filters import BaseFilterBackend


class FaultPlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaultPlans
        fields = '__all__'