import time
import airsim
import math
from base_service import *
from cache.config import IP
import numpy as np

# 连接到AirSim模拟器，定义了一个client_pip用于UE创建管道
client_pip = airsim.MultirotorClient(IP)
client_pip.confirmConnection()


def pip_cre_with_color(client, node1, node2, node1_name, node2_name, color, width=15, height=20):
    """创建航路管道，输入为航路两端节点坐标、名称、管道颜色"""
    # 计算节点之间的距离
    length = math.sqrt((node2[0] - node1[0])**2 + (node2[1] - node1[1])**2)

    # 设置飞行路径的尺度
    pip_scale = airsim.Vector3r(length-20*math.sqrt(3), width, height)

    # 计算飞行路径的中心点
    pip_cen = [(node2[0] + node1[0]) / 2, (node2[1] + node1[1]) / 2, node1[2]]  # 高度保持不变

    # 计算方向向量并转换为四元数
    pip_dir = [node2[0] - node1[0], node2[1] - node1[1], 0]
    pip_orientation = vector_to_quaternion(pip_dir)

    # 设置飞行路径的姿态
    pip_pose = airsim.Pose(airsim.Vector3r(pip_cen[0], pip_cen[1], pip_cen[2]),
                           pip_orientation)

    # 通过AirSim模拟器添加管道到UE
    client.addFlightPip(f'{node1_name}to{node2_name}', pip_pose, pip_scale, color, cube=True)
    print(f'{node1_name}to{node2_name}')


def vector_to_quaternion(v):
    """将方向向量转换为四元数"""
    # 归一化方向向量
    v_mag = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
    if v_mag == 0:
        return airsim.Quaternionr(0, 0, 0, 1)  # 如果向量为零向量，返回单位四元数

    v_normalized = [v[0] / v_mag, v[1] / v_mag, v[2] / v_mag]

    # 计算与Z轴的夹角
    yaw = math.atan2(v_normalized[1], v_normalized[0])

    # 将偏航角转换为四元数
    qw = math.cos(yaw / 2)
    qz = math.sin(yaw / 2)

    return airsim.Quaternionr(0, 0, qz, qw)


def port_cre(node):
    """创建机场管道"""
    # 机场管道姿态
    port_pose = airsim.Pose(airsim.Vector3r(node[0],node[1],-60),airsim.Quaternionr(0,0,0,1))
    # 机场管道大小
    port_scale = airsim.Vector3r(50,50,120)
    # 机场管道颜色
    port_color = [0.4, 0.843, 0.608, 0.8]
    # 通过AirSim模拟器添加管道到UE
    client_pip.addFlightPip(f"{node}", port_pose, port_scale, port_color, cube=False)


def dynamic_change_pipe(pip_name):  # 这个函数不涉及管控可以跳过，功能还不完善
    """管控航路管道颜色更改"""
    node_names = pip_name.split('to')

    nodes = []

    color2 = [1, 0, 0, 0.5]

    # 遍历分割后的字符串列表
    for node_name in node_names:
        # 去掉方括号并分割字符串以获取坐标值
        coords = node_name.strip('[]').split(',')
        # 将坐标值转换为整数列表
        node = list(map(lambda x: int(float(x)), coords))
        # 将转换后的点添加到点列表中
        nodes.append(node)

    client_pip.delFlightPip(pip_name)
    pip_cre_with_color(client_pip, node1=nodes[0], node2=nodes[1], node1_name=node_names[1], node2_name=node_names[0], color=color2)


# # 添加航路管道
color1 = [0.29, 0.729, 1, 0.65]  # 设置颜色
nodes_dict = dict.fromkeys(nodes_list)  # 根据节点id列表，创建一个字典，key为节点id，value为节点三维坐标列表[x,y,z]
pip_flag = {}  # 用于标注航路管道是否被创建（双向航路在数据库中，存储为两条航路数据，但管道只需创建一次，防止重复创建管道）
for edge in edges_dict:  # 遍历航路字典
    [start_node_id, end_node_id] = edges_dict[edge]  # 获取航路的起始节点和终止节点id
    # 获取起始节点和终止节点的三维坐标（航路坐标点的第一个点和最后一个点，对应了起始节点和终止节点坐标）
    [start_node, end_node] = [net[start_node_id][end_node_id][1][0], net[start_node_id][end_node_id][1][-1]]
    if f'{end_node}to{start_node}' in pip_flag:  # 确保 还未创建 与该航路反向的航路管道
        continue
    # 通过Airsim模拟器,创建航路管道到UE
    pip_cre_with_color(client_pip, start_node, end_node, f'{start_node}', f'{end_node}', color1)
    pip_flag[f'{start_node}to{end_node}'] = 1  # 标注已创建该航路管道
    nodes_dict[start_node_id] = start_node  # 将节点坐标信息存入nodes_dict字典
    nodes_dict[end_node_id] = end_node  # 将节点坐标信息存入nodes_dict字典
    time.sleep(0.1)


# # 添加圆柱形节点
cir_scale = airsim.Vector3r(40, 40, 20)  # 设置节点管道大小
# cir_color = [0.976, 0.973, 0.422, 0.65]
cir_color = [0.29, 0.729, 1, 0.65]  # 设置节点管道颜色
for node_id in nodes_list:  # 遍历每个节点
    # 生成每个节点的名称，如 'circle1', 'circle2', 等
    circle_name = f"circle{node_id}"
    # 设置节点的位置
    cir_pose = airsim.Pose(airsim.Vector3r(nodes_dict[node_id][0], nodes_dict[node_id][1], nodes_dict[node_id][2]),
                           airsim.Quaternionr(0, 0, 0, 1))

    # 调用 addFlightPip 函数
    client_pip.addFlightPip(circle_name, cir_pose, cir_scale, cir_color, cube=False)
    time.sleep(0.1)


# # 添加机场
airports_keys = cdb_client.rdb.keys(pattern=f'{proposal_id}:airport:*')  # 获取redis中的所有机场key值
for airport_key in airports_keys:  # 遍历所有机场key值
    value = cdb_client.get_data(airport_key)  # 根据key从redis读取该机场信息
    airport_gps = value['gps']  # 获取机场二维坐标，格式为字符串'(x,y)'
    airport_name = value['name']  # 获取机场名称
    airport_gps_xy = (airport_gps.strip('()')).split(',')  # 提取坐标信息
    airport_gps_xy = [float(i) for i in airport_gps_xy]  # 将坐标信息由字符串转换为数值float
    ports_pos[airport_name] = np.array(airport_gps_xy)  # 将二维坐标列表转换为向量，存入ports_pos字典，key为无人机名称
    # 在UE中创建机场实体
    loc = airsim.Vector3r(airport_gps_xy[0], airport_gps_xy[1], 0)
    client_pip.addLandingPort(airport_name, loc, 10)
    # 在UE中创建圆柱形机场管道
    port_cre(airport_gps_xy + [-120])

# # 定义每个机场停放无人机的停放点位置
add_places = [  # 定义以(0,0,0)为基准，机场内部停放无人机的位置
    [0, 2, 0], [2, 0, 0], [0, -2, 0], [-2, 0, 0],
    [2, 2, 0], [2, -2, 0], [-2, -2, 0], [-2, 2, 0],
    [0, 4, 0], [4, 0, 0], [0, -4, 0], [-4, 0, 0]
]
places = dict.fromkeys(ports_pos)  # 创建字典，存储每个机场内部停放无人机的位置，key为无人机名称
for airport in places:  # 遍历places
    places[airport] = []  # 初始化为列表
    # 根据add_places，将基准由(0,0,0)平移到机场中心(x,y,0)，将该机场(x,y)内部停放无人机的位置存入places
    for add_place in add_places:
        places[airport] = places[airport] + [(np.array(add_place)+np.append(ports_pos[airport], 0)).tolist()]
# 每个机场定义一个队列，用于给无人机随机分配停放位置
que = dict.fromkeys(places.keys(), None)
for key in que:
    que[key] = [x for x in range(len(places[key]))]

