from rest_framework import serializers

from source.road_control.models import RoadControl
from rest_framework.filters import BaseFilterBackend


class RoadControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadControl
        fields = '__all__'