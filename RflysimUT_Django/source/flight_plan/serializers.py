from rest_framework import serializers

from source.flight_plan.models import FlightRequirements
# from rest_framework.filters import BaseFilterBackend
#
# from source.uav.serializers import DronesSerializer
# from source.air_road.serializers import AirportsSerializer
# from source.proposal.serializers import ProposalsSerializer


class FlightRequirementsSerializer(serializers.ModelSerializer):
    # flight_path = serializers.CharField()
    # airway_path = serializers.CharField()

    # start_airport = AirportsSerializer()
    # end_airport = AirportsSerializer()
    # drone = DronesSerializer()
    # proposal = ProposalsSerializer()
    start_airport_name = serializers.SerializerMethodField()
    end_airport_name = serializers.SerializerMethodField()
    drone_name = serializers.SerializerMethodField()
    proposal_name = serializers.SerializerMethodField()
    class Meta:
        model = FlightRequirements
        fields = '__all__'
        extra_fields = ['start_airport_name','end_airport_name','drone_name','proposal_name']  # 添加自定义字段

    def get_start_airport_name(self, obj):
        return obj.start_airport.name  # 获取 author 外键的 name 字段

    def get_end_airport_name(self, obj):
        return obj.end_airport.name  # 获取 author 外键的 name 字段


    def get_drone_name(self, obj):
        return obj.drone.name  # 获取 author 外键的 name 字段

    def get_proposal_name(self, obj):
        return obj.proposal.name  # 获取 author 外键的 name 字段

    def to_representation(self, instance):
        redis_flag = self.context.get('redis_flag', False)        
        data = super().to_representation(instance)
        
        # 如果redis_flag为True，则添加额外的字段
        if redis_flag:
            data['flight_path'] = "[]"
            data['airway_path'] = "[]"        
        return data