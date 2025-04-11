from rest_framework import serializers

from source.air_road.models import Permissions, Layers, Nodes, Edges, Airports
from rest_framework.filters import BaseFilterBackend


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = '__all__'


class LayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layers
        fields = '__all__'

class EdgesSerializer(serializers.ModelSerializer):
    # redis存储额外的序列化字段
    # flow_velocity = serializers.FloatField()
    # density = serializers.FloatField()
    # PeriodTTT = serializers.IntegerField()
    # PeriodTTD = serializers.IntegerField()
    # PeriodNum = serializers.IntegerField()

    class Meta:
        model = Edges
        fields = '__all__'

    def to_representation(self, instance):
        redis_flag = self.context.get('redis_flag', False)        
        data = super().to_representation(instance)
        
        # 如果redis_flag为True，则添加额外的字段
        if redis_flag:
            data['flow_velocity'] = 0.0
            data['density'] = 0.0
            data['PeriodTTT'] = 0
            data['PeriodTTD'] = 0
            data['PeriodNum'] = 0
        
        return data
    
class NodesSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Nodes
        fields = '__all__'


class AirportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airports
        fields = '__all__'


