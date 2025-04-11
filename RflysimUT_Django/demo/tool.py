import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))


def distance(points):
    """路径规划时每条边的权值计算函数"""
    return 1


def create_net(cdb_client, proposal_id):
    """创建航路网结构"""
    edge_keys = cdb_client.rdb.keys(pattern=f'{proposal_id}:airway:*')
    net = {}
    nodes_list = []
    edges_dict = {}
    for edge_key in edge_keys:
        edge_data = cdb_client.get_data(edge_key)
        start_node = (edge_data['start_node'])
        end_node = (edge_data['end_node'])
        nodes_list = nodes_list + [start_node] + [end_node]
        edge_data['nodes'] = edge_data['nodes'].split(';')
        edge_points = []
        for node in edge_data['nodes']:
            node = node.strip('()').split(",")
            node = [float(x.strip('()')) for x in node]
            edge_points.append(node)
        if not net.get(start_node, None):
            net[start_node] = {}
        net[start_node][end_node] = [edge_data['id'], edge_points, distance(edge_points)]
        edges_dict[edge_data['id']] = [start_node, end_node]
    nodes_list = list(set(nodes_list))
    return [net, nodes_list, edges_dict]


def get_flight_requirements(cdb_client, proposal_id):
    """读取redis中的flight_requirements数据"""
    keys = cdb_client.rdb.keys(pattern=f'{proposal_id}:flight_requirement:*')
    flight_requirements = []
    for key in keys:
        value = cdb_client.get_data(key)
        start_airport_id = value['start_airport']
        end_airport_id = value['end_airport']
        drone_id = value['drone']
        flight_requirement_id = value['id']
        start_airport_data = cdb_client.get_data(f"{proposal_id}:airport:{start_airport_id}")
        end_airport_data = cdb_client.get_data(f"{proposal_id}:airport:{end_airport_id}")
        start_airport_name = start_airport_data['name']
        end_airport_name = end_airport_data['name']
        value['start_airport_name'] = start_airport_name
        value['end_airport_name'] = end_airport_name
        start_node_id = start_airport_data['exit_node']
        end_node_id = end_airport_data['entrance_node']
        flight_requirements = flight_requirements + [[flight_requirement_id, drone_id,
                                                      start_node_id, end_node_id, value]]
    return flight_requirements


def djstra(net, nodes_list, start_node, end_node):
    """路径规划算法"""
    MAX = 0x3f
    flag = dict.fromkeys(nodes_list, False)  # 记录每个节点是否被标记
    min_distance = dict.fromkeys(nodes_list, MAX)  # 记录每个节点的最短距离
    min_distance[start_node] = 0
    pre_node = dict.fromkeys(nodes_list, None)  # 记录每个节点在最优路径中的前节点
    for i in range(len(nodes_list)):
        temp = -1
        for node in nodes_list:
            if (not flag[node]) and (temp == -1 or min_distance[node] < min_distance[temp]):
                temp = node
        if net.get(temp, False):
            for node in net[temp].keys():
                if min_distance[node] > (min_distance[temp] + net[temp][node][2]):
                    min_distance[node] = min_distance[temp] + net[temp][node][2]
                    pre_node[node] = temp
        else:
            return False
        flag[temp] = True
    # 生成轨迹
    node_j = end_node
    node_i = node_j
    points = []
    edges = []
    nodes = [end_node]
    while not (node_i == start_node):
        node_i = pre_node[node_j]
        if node_i == start_node:
            points = net[node_i][node_j][1] + points
        else:
            points = net[node_i][node_j][1][1:] + points
        edges = [net[node_i][node_j][0]] + edges
        node_j = node_i
        nodes = [node_i] + nodes
    return [points, edges, nodes]


def refresh_drone(cdb_client, proposal_id, drone_id, initial_pos, position, edge_id):
    """将无人机的初始位置、无人机名称、当前位置、所在航路id更新到redis"""
    key = f"{proposal_id}:drone_current:{drone_id}"
    value = {}
    value['position'] = position
    value['edge'] = edge_id
    value['name'] = f'drone_{drone_id}'
    value['initial_position'] = initial_pos
    cdb_client.set_data(key, value, None)


def get_network_control(cdb_client, proposal_id):
    """获取redis中的管控数据"""
    keys = cdb_client.rdb.keys(pattern=f'{proposal_id}:network_control:*')
    network_controls = {}
    for key in keys:
        value = cdb_client.get_data(key)
        edge_id = value['edge']
        control_type = value['type']
        network_controls[edge_id] = control_type
    return network_controls


def get_drones(cdb_client, proposal_id):
    """获取redis中的无人机数据"""
    keys = cdb_client.rdb.keys(pattern=f'{proposal_id}:drone:*')
    drones = {}
    for key in keys:
        value = cdb_client.get_data(key)
        drone_id = value['id']
        drones[drone_id] = None
    return drones


def plan_a_new_path(net, nodes_list, start_node, end_node, network_controls, edges_dict):
    """结合管控数据进行路径规划"""
    for edge_ctrl in network_controls:
        if network_controls[edge_ctrl] == 1:
            [edge_start_node, edge_end_node] = edges_dict[edge_ctrl]
            del net[edge_start_node][edge_end_node]
        else:
            pass  # add velocity limit in the future
    return djstra(net, nodes_list, start_node, end_node)
