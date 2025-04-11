import os
import django
import redis
import json
from cache.redis_key import *
from cache.redis_db import redis_db as rdb
from cache.config import *

proposal_id = 1


def write_airway_to_redis(redis_client):
    from source.air_road.models import Permissions, Layers, Nodes, Edges, Airports
    edges = Edges.objects.all()

    for edge in edges:
        proposal_id = edge.proposal.id
        airway_id = edge.id
        airway_dict = {
            'id': edge.id,
            'start_node': edge.start_node.id,
            'end_node': edge.end_node.id,
            'nodes': edge.nodes,
            'lanes': edge.lanes,
            'permission': edge.permission.id,
            'max_cross': edge.max_cross,
            'max_speed': edge.max_speed,
            'length': edge.length,
            'height': edge.height,
            'volume': edge.volume,
            'junction': edge.junction,
            'rule': edge.rule,
            # 'flow_velocity': edge.flow_velocity,
            # 'density': edge.density,
            # 'periodTTT': edge.periodTTT,
            # 'periodTTD': edge.periodTTD,
            # 'periodNum': edge.periodNum,
        }
        cache_key = AIRWAY_KEY.format(proposal_id, airway_id)
        redis_client.set_data(cache_key, airway_dict, None)

def write_node_to_redis(redis_client):
    from source.air_road.models import Permissions, Layers, Nodes, Edges, Airports
    nodes = Nodes.objects.all()

    for node in nodes:
        proposal_id = node.proposal.id
        node_id = node.id
        node_dict = {'id': node.id,
                     'type': node.type,
                     'layer': node.layer.id,
                     'connections': node.connections,
                     'permission': node.permission.id if node.permission else None,
                     'max_cross': node.max_cross,
                     'max_speed': node.max_speed,
                     'position': node.gps,
        }
        cache_key = NODE_KEY.format(proposal_id, node_id)
        redis_client.set_data(cache_key, node_dict, None)

def write_airport_to_redis(redis_client):
    from source.air_road.models import Airports
    airports = Airports.objects.all()
    for airport in airports:
        proposal_id = airport.proposal.id
        airport_id = airport.id
        airport_dict = {'id': airport.id,
                        'proposal': airport.proposal.id,
                        'name': airport.name,
                        'gps': airport.gps,
                        'radius': airport.radius,
                        'entrance_node': airport.entrance_node.id,
                        'exit_node': airport.exit_node.id,
                        'permission': airport.permission.id,
                        'max_speed ': airport.max_speed,
                        'capacity': airport.capacity,
                        }
        cache_key = AIRPORT_KEY.format(proposal_id, airport_id)
        redis_client.set_data(cache_key, airport_dict, None)

def write_uav_data_to_redis(redis_client):
    from source.uav.models import Drones
    drones = Drones.objects.all()
    for drone in drones:
        drone_id = drone.id
        proposal_id = drone.proposal.id
        drone_dict={'id': drone.id,
                    'proposal': drone.proposal.name,
                    'name': drone.name,
                    'max_speed': drone.max_speed,
                    'model': drone.model,
                    'serial_number': drone.serial_number,
                    'manufacturer': drone.manufacturer,
                    'manufacturer_date': drone.manufacturer_date.isoformat() if drone.manufacturer_date else None,
                    'registration_date ': drone.registration_date.isoformat() if drone.registration_date else None,
                    'max_flight_time': drone.max_flight_time,
                    'battery_capacity': drone.battery_capacity,
                    'payload_capacity': drone.payload_capacity,
                    'weight': drone.weight,
                    'camera_resolution': drone.camera_resolution,
                    'safe_radius': drone.safe_radius,
                    }
        cache_key = DRONE_KEY.format(proposal_id, drone_id)
        redis_client.set_data(cache_key, drone_dict, None)

def write_flight_requirement_to_redis(redis_client):
    from source.flight_plan.models import FlightRequirements
    flight_requirements = FlightRequirements.objects.all()
    for flight_requirement in flight_requirements:
        proposal_id = flight_requirement.proposal.id
        flight_requirement_id = flight_requirement.id
        flight_plan_dict={'id': flight_requirement.id,
                          'proposal': flight_requirement.proposal.id,#导入Airports模块
                          'name': flight_requirement.name,
                          'drone': flight_requirement.drone.id,#导入Drones模块
                          'start_time': flight_requirement.start_time.strftime('%H:%M:%S'),
                          'end_time': flight_requirement.end_time.strftime('%H:%M:%S'),
                          'duration': flight_requirement.duration,
                          'priority': flight_requirement.priority,
                          'start_airport': flight_requirement.start_airport.id,#导入Airports模块
                          'end_airport': flight_requirement.end_airport.id,#导入Airports模块
                          'type': flight_requirement.type,
        }
        cache_key = FLIGHT_REQUIREMENT_KEY.format(proposal_id, flight_requirement_id)
        redis_client.set_data(cache_key, flight_plan_dict, None)


def write_network_control_to_redis(redis_client):
    from source.road_control.models import RoadControl
    road_controls = RoadControl.objects.all()

    for road_control in road_controls:
        proposal_id = road_control.proposal_id
        RoadControl_id = road_control.id
        RoadControl_dict = {'id': road_control.id,
                            'type': road_control.type,
                            'min_value': road_control.min_value,
                            'max_value': road_control.max_value,
                            'edge': road_control.edge.id,
                            'start_time': road_control.start_time.strftime('%H:%M:%S'),
                            'end_time': road_control.end_time.strftime('%H:%M:%S'),
                            'duration': road_control.duration,
        }
        cache_key = NETWORK_CONTROL_KEY.format(proposal_id, RoadControl_id)
        redis_client.set_data(cache_key, RoadControl_dict, None)


# def write_place_to_redis(redis_client):
#     from cache.place import place_pos
#     key = f'{proposal_id}:place:1'
#     redis_client.set_data(key, place_pos, None)


def refresh_redis(redis_client):
    # write_airway_to_redis(redis_client)
    # write_airport_to_redis(redis_client)
    # write_node_to_redis(redis_client)
    write_flight_requirement_to_redis(redis_client)
    write_network_control_to_redis(redis_client)
    # print("Redis refreshed")


def write_to_redis(redis_client):
    write_airway_to_redis(redis_client)
    write_airport_to_redis(redis_client)
    write_node_to_redis(redis_client)
    write_flight_requirement_to_redis(redis_client)
    write_network_control_to_redis(redis_client)
    # write_place_to_redis(redis_client)
    print("Data has been written to redis")

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RflysimUT.settings")
# django.setup()
# cdb_client = rdb(host=G_REDIS_HOST, port=G_REDIS_PORT, db=G_REDIS_DB, password=G_REDIS_PW)
# write_airway_to_redis(cdb_client)
# write_node_to_redis(cdb_client)
# write_airport_to_redis(cdb_client)
# write_flight_requirement_to_redis(cdb_client)
# write_uav_data_to_redis(cdb_client)
# write_place_to_redis(cdb_client)
