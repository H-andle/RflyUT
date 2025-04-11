from pip_service import *


def listen():
    global flight_requirements, net, proposal_id, nodes_list, network_controls, edges_dict, nodes_dict, drones, \
        drones_id, cdb_client, drone_db, takeoff_ports, land_ports
    while True:
        # 更新redis（将数据库信息同步到redis）
        refresh_redis(cdb_client)
        # 更新无人机信息
        drones_temp = get_drones(cdb_client, proposal_id)
        drones_id = drones_temp.keys()

        # from requirement to plan （根据requirement进行路径规划，如需自定义路径规划可以更改djstra函数）
        flight_requirements_new = get_flight_requirements(cdb_client, proposal_id)  # 从redis获取新的requirement信息
        if not len(flight_requirements_new) == len(flight_requirements):  # if 有新的requirement
            for new_req in flight_requirements_new:
                if new_req not in flight_requirements:
                    [points, edges, nodes] = djstra(net, nodes_list, new_req[2], new_req[3])  # 路径规划，输出路径坐标点列表、路径途经航路id、路径途经节点id
                    new_req[4]['flight_path'] = points  # 将路径坐标点添加到requirement中
                    new_req[4]['airway_path'] = edges  # 将路径途经航路添加到requirement中
                    takeoff_ports[new_req[1]] = new_req[4]['start_airport_name']  # 获取起飞机场名称，存入takeoff_ports字典
                    land_ports[new_req[1]] = new_req[4]['end_airport_name']  # 获取降落机场名称，存入land_ports字典
                    drones[new_req[1]] = [points, edges, nodes, new_req[0]]  # 将路径信息存入drones字典，便于后续对无人机进行控制调度
                    print(new_req[1])  # 打印无人机id
                    print(drones[new_req[1]])  # 打印该无人机drones信息
                    cdb_client.set_data(f'{proposal_id}:flight_plan:{new_req[0]}', new_req[4], None)  # 将plan信息存入redis(plan即为requirement基础上增加了规划好的路径信息)
        flight_requirements = flight_requirements_new

        # refresh network control （下面的代码开发不完善，可跳过不看）
        network_controls = get_network_control(cdb_client, proposal_id)
        for ctrl in network_controls:
            if network_controls[ctrl] == 0:
                del network_controls[ctrl]
            elif (not network_controls_flag.get(ctrl, False)) or \
                    (network_controls[ctrl] != network_controls_flag[ctrl]):
                if network_controls[ctrl] == 1:
                    [start_node_id, end_node_id] = edges_dict[ctrl]
                    dynamic_change_pipe(f'{nodes_dict[start_node_id]}to{nodes_dict[end_node_id]}')
                    network_controls_flag[ctrl] = 1

        # from network control to plan （结合管控信息进行路径规划，如需自定义路径规划可以更改djstra函数）
        for drone in drones:
            flag_ctrl = 0
            if len(drones[drone][1]) < 2:
                continue
            for edge in drones[drone][1][1:]:
                if network_controls.get(edge, False) and network_controls[edge] == 1:
                    flag_ctrl = 1
            if flag_ctrl == 1:
                print(f'drone_{drone} needs to plan a new path due to network control')
                drones[drone] = plan_a_new_path(net, nodes_list, drones[drone][2][0], drones[drone][2][-1],
                                                network_controls, edges_dict)
        time.sleep(1)

