from redis_db import redis_db as rdb
from redis_key import *
from config import *
import json

cdb_client = rdb(host=G_REDIS_HOST, port=G_REDIS_PORT, db=G_REDIS_DB, password=G_REDIS_PW)    # control system local db
mdb_client = rdb(host=G_REDIS_HOST, port=G_REDIS_PORT, db=G_REDIS_DB, password=G_REDIS_PW)    # manage system local db
sdb_client = rdb(host=G_REDIS_HOST, port=G_REDIS_PORT, db=G_REDIS_DB, password=G_REDIS_PW)    # shared db

def get_airway_from_cache(proposal_id,airway_id):
    cache_key = AIRWAY_KEY.format(proposal_id,airway_id)
    cached_data = sdb_client.get_data(cache_key)
    return cached_data

def set_airway_to_cache(proposal_id, airway_id, data:json, ex):
    cache_key = AIRWAY_KEY.format(proposal_id,airway_id)
    sdb_client.set_data(cache_key, data, ex=ex)

def set_node_to_cache(proposal_id,node_id, data:json, ex):
    cache_key = NODE_KEY.format(proposal_id, node_id)
    sdb_client.set_data(cache_key, data, ex=ex)

def set_airport_to_cache(proposal_id,airport_id, data:json, ex):
    cache_key = AIRPORT_KEY.format(proposal_id, airport_id)
    sdb_client.set_data(cache_key, data, ex=ex)

def get_drone_from_cache(proposal_id,airway_id):
    cache_key = DRONE_KEY.format(proposal_id, airway_id)
    cached_data = sdb_client.get_data(cache_key)
    return cached_data

def set_drone_to_cache(proposal_id,drone_id, data:json, ex):
    cache_key = DRONE_KEY.format(proposal_id, drone_id)
    sdb_client.set_data(cache_key, data, ex=ex)

def set_requirement_to_cache(proposal_id,requirement_id, data:json, ex):
    cache_key = FLIGHT_REQUIREMENT_KEY.format(proposal_id, requirement_id)
    mdb_client.set_data(cache_key, data, ex=ex)