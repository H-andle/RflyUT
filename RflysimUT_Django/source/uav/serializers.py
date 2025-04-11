from rest_framework import serializers

from source.uav.models import Drones
from rest_framework.filters import BaseFilterBackend


class DronesSerializer(serializers.ModelSerializer):
    # condition = serializers.IntegerField() # 状态（0-停放，1-起飞，2-飞行，3-降落，4-充电）
    # enable_time = serializers.DateTimeField()
    # finish_time = serializers.DateTimeField()
    # flight_path = serializers.CharField()    
    # node_arrive_time = serializers.CharField()
    # pos = serializers.CharField()
    # vel = serializers.CharField()
    # vel_ver = serializers.CharField()
    # velocity_com = serializers.CharField()
    # velocity_com_ver = serializers.CharField()
    # current_waypoint = serializers.IntegerField()
    # current_airway = serializers.IntegerField()
    # lane = serializers.IntegerField()
    # travel_time = serializers.IntegerField()
    # travel_distance = serializers.FloatField()

    class Meta:
        model = Drones
        fields = '__all__'

    def to_representation(self, instance):
        redis_flag = self.context.get('redis_flag', False)        
        data = super().to_representation(instance)
        
        # 如果redis_flag为True，则添加额外的字段
        if redis_flag:
            data['condition'] = 0
            data['enable_time'] = 0
            data['finish_time'] = 0
            data['node_arrive_time'] = "[]"
            data['pos'] = ""
            data['vel'] = ""
            data['vel_ver'] = 0
            data['vel_com'] = 0
            data['vel_com_ver'] = 0
            data['current_waypoint'] = 0
            data['current_airway'] = 0
            data['lane'] = 1
            data['travel_time'] = 0
            data['travel_distance'] = 0        
        return data