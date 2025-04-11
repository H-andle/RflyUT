from django.shortcuts import render
from rest_framework import viewsets

from source.uav.models import Drones
from source.uav.serializers import DronesSerializer
from cache.config import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from cache.redis_db import redis_db as rdb

class DroneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Drones.objects.all()
    serializer_class = DronesSerializer

@api_view(['GET'])
def get_drones_state(request):
    """
    获取无人机状态，例如飞行中的无人机个数，待起飞的无人机个数等
    """
    if request.method == 'GET':
        in_flight_num = 0
        waiting_flight_num = 0
        proposal_id = 1
        cdb_client = rdb(host=G_REDIS_HOST, port=G_REDIS_PORT, db=G_REDIS_DB, password=G_REDIS_PW)
        req_keys = cdb_client.rdb.keys(pattern=f'{proposal_id}:flight_requirement:*')
        plan_keys = cdb_client.rdb.keys(pattern=f'{proposal_id}:flight_plan:*')
        drone_db = rdb(host=G_REDIS_HOST, port=G_REDIS_PORT, db=G_REDIS_DB + 1, password=G_REDIS_PW)
        drones_pos_keys = drone_db.rdb.keys(pattern=f'{proposal_id}:drone_current:*')
        for key in drones_pos_keys:
            key = key.decode('utf-8')
            key = key.split(':')[-1]
            value = drone_db.get_data(f'{proposal_id}:drone_current:{key}')
            if value['edge'] != -1:
                in_flight_num += 1
            else:
                waiting_flight_num += 1

        finished_req_num = len(plan_keys) - in_flight_num
        if finished_req_num < 0:
            finished_req_num = 0

        # return Response([in_flight_num, waiting_flight_num, in_req_num, finished_req_num], status=200)
        return Response({"waiting": 22, "flying": 9, "finished": 39, "birang": 5,
                         "denied": 0, "canceled": 0}, status=200)
    else:
        return Response({"message": "Invalid request", "code": 400}, status.HTTP_400_BAD_REQUEST)
