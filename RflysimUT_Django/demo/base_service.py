from tool import *
from cache.write_to_redis import refresh_redis
from cache.write_to_redis import write_to_redis
from cache.redis_db import redis_db as rdb
from cache.config import *
import django


# 初始化django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RflysimUT.settings")
django.setup()
from source.proposal.models import Proposals
# 连接到redis
cdb_client = rdb(host=G_REDIS_HOST, port=G_REDIS_PORT, db=G_REDIS_DB, password=G_REDIS_PW) # 存储数据库数据的redis库
drone_db = rdb(host=G_REDIS_HOST, port=G_REDIS_PORT, db=G_REDIS_DB + 1, password=G_REDIS_PW) # 存储无人机实时信息的redis库
# 清空redis残余数据
cdb_client.rdb.flushall()
drone_db.rdb.flushall()
# 将初始数据库数据写入redis
write_to_redis(cdb_client)

# 定义仿真方案的id
proposal = Proposals.objects.get(name='proposal')
proposal_id = proposal.id
# 创建航路网
[net, nodes_list, edges_dict] = create_net(cdb_client, proposal_id)
# 定义flight_requirements
flight_requirements = []
# 定义network_controls 以及标记管控是否已经作用过的flag
network_controls = {}
network_controls_flag = {}
# 获取无人机数据
drones = get_drones(cdb_client, proposal_id)
drones_id = drones.keys()
# 定义无人机的起始创建位置、终点位置
initial_positions = {}
final_positions = {}
# 定义无人机当前任务的出发位置
start_positions = {}
# 存储无人机实时位置信息的字典
drones_pos = {}
# 定义字典，用于存储每个无人机当前任务的起飞、降落机场
takeoff_ports = {}
land_ports = {}
# 定义存储机场坐标的字典
ports_pos = {}
# 定义已完成飞行任务的无人机队列，用于自动生成新的飞行任务
finish_que = []

