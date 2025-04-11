from rest_framework import serializers

from source.experiment.models import Experiments,EdgeLogs,FlightLogs
from rest_framework.filters import BaseFilterBackend

class ExperimentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiments
        fields = '__all__'


class EdgeLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EdgeLogs
        fields = '__all__'

class FlightLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightLogs
        fields = '__all__'