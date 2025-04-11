from rest_framework import serializers
from .models import ClickAirport, ClickNode, ClickEdge

class ClickAirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClickAirport
        fields = '__all__'


class ClickNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClickNode
        fields = '__all__'


class ClickEdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClickEdge
        fields = '__all__'
