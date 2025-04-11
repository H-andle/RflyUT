import time
import threading
from listen_service import *
import numpy as np
from parameter import *
from cache.config import IP


def mysat(val, max_val):
    norm_val = np.linalg.norm(val)
    if norm_val > max_val:
        return val * max_val / norm_val
    return val


# 创建clients字典，存储每个无人机的client，key为无人机id
clients = {}


def run(client, drone, num):
    global drones, drones_id, drones_pos
    flag_first = True  # 标注无人机还未开始飞行
    client.pickBox(f'drone_{drone}', takeoff_ports[drone])  # 执行取货动作
    time.sleep(10)  # 等待取货动作完成
    client.moveToPositionAsync(start_positions[drone].x_val-initial_positions[drone].x_val,
                               start_positions[drone].y_val-initial_positions[drone].y_val, -120, 10,
                               vehicle_name=f'drone_{drone}')
    if drones[drone]:  # if 该无人机的路径信息不为空，即该无人机有未完成的飞行任务
        drones[drone][0].pop(0)  # 弹出路径途经的第一个坐标点（因为路径的第一个坐标与起点机场重合，视为已到达）
        drones[drone][2].pop(0)  # 弹出路径途经的第一个节点id（因为路径的第一个节点与起点机场坐标重合，视为已到达）
        velocity = np.array([0.0, 0.0, 0.0])  # 初始化速度向量为0
        while drones[drone][0]:
            # 更新无人机当前位置
            position = clients[drone].getMultirotorState(
                vehicle_name=f'drone_{drone}').kinematics_estimated.position
            while flag_first:  # 若无人机还未开始飞行，先等待无人机升空到指定高度
                # 确保无人机升空到指定高度
                position = clients[drone].getMultirotorState(
                    vehicle_name=f'drone_{drone}').kinematics_estimated.position
                if position.z_val < -110:  # if 高度<-110（z轴正方向朝下）
                    flag_first = False
                    que[takeoff_ports[drone]].append(num)  # 解放将该无人机起飞时占用的机场空位
                    break
                time.sleep(1)
            # 更新无人机实时位置信息到drones_pos字典，key为无人机id
            drones_pos[drone] = [position.x_val + initial_positions[drone].x_val,
                                 position.y_val + initial_positions[drone].y_val,
                                 position.z_val + initial_positions[drone].z_val]
            position = np.array(drones_pos[drone])  # 定义无人机位置向量
            target = np.array(drones[drone][0][0])  # 定义无人机下一个飞行目标点位置向量

            # 吸引力方向：无人机与当前目标点的向量
            el = target - position
            el_norm = np.linalg.norm(el)
            if el_norm != 0:
                attract_force = K_attract * (el / el_norm)  # 吸引力与目标点距离成正比
            else:
                attract_force = np.array([0.0, 0.0, 0.0])

            # 计算与其他无人机的斥力
            repulsion = 0  # 初始化斥力为0
            other_drones = drones_pos.copy()  # 复制所有无人机实时位置信息，防止后续遍历过程中，有新的无人机生成，导致drones_pos被修改报错
            for other_drone in other_drones:  # 遍历所有无人机位置
                if drone == other_drone:  # 只遍历其他无人机，跳过该无人机
                    continue
                if other_drone in drones_pos:  # 如果遍历到的无人机，没有结束飞行任务，在ports_pos中存在
                    direction = position - np.array(drones_pos[other_drone])  # 计算两无人机之间的位置差向量
                distance = np.linalg.norm(direction)  # 计算两无人机之间的距离
                if 0 < distance < rs:  # 避障范围，距离<rs时，进行紧急避障
                    repulsion_magnitude = K_repulse * (rs - distance) ** 3 / (distance ** 2)  # 两无人机避障所需斥力
                    repulsion += repulsion_magnitude * (direction / distance)  # 叠加在总斥力上
                elif rs <= distance < ra:  # 增加一个平滑过渡的区域
                    repulsion_magnitude = 1 * K_repulse * (ra - distance) / (ra - rs)
                    repulsion += repulsion_magnitude * (direction / distance)

            # 合力
            total_force = attract_force + repulsion
            # 平滑速度更新 (插值)
            velocity = 0.5 * velocity + 0.5 * mysat(total_force, vmax)
            vx, vy, vz = velocity
            # 通过Airsim模拟器，执行速度控制指令
            clients[drone].moveByVelocityAsync(vx, vy, vz, time_step*1.5, vehicle_name=f'drone_{drone}')

            # 检查是否到达当前目标点
            distance_to_target = np.linalg.norm(target - position)
            if distance_to_target < 15 and len(drones[drone][0]) > 0:  # 若到达目标点，且drones中该无人机路径信息不为空
                drones[drone][0].pop(0)  # 弹出一个路径坐标点，表示已到达该坐标点
                drones[drone][1].pop(0)  # 弹出一个路径途经航路id，表示已经过该航路
                drones[drone][2].pop(0)  # 弹出一个路径途经节点id，表示已到达该节点
                if len(drones[drone][0]) == 0:  # if 该无人机在drones中的路径信息为空，说明已到达终点
                    while not que[land_ports[drone]]:  # if 终点机场内无人机已满，不存在空余的位置
                        time.sleep(1)  # 等待直至有空余的位置用于停放该无人机
                    num = que[land_ports[drone]].pop(0)  # 从机场内的位置队列中弹出一个，用于停放该无人机
                    # 将无人机完成当前飞行任务后，最终停下的位置坐标存入final_positions
                    final_positions[drone] = airsim.Vector3r(places[land_ports[drone]][num][0],
                                                             places[land_ports[drone]][num][1],
                                                             places[land_ports[drone]][num][2])
                    # 控制无人机移动到最终位置上方5m处
                    client.moveToPositionAsync(final_positions[drone].x_val-initial_positions[drone].x_val,
                                               final_positions[drone].y_val-initial_positions[drone].y_val, -5, 10,
                                               vehicle_name=f'drone_{drone}')
                    time.sleep(20)  # 等待到达指定位置
                    # 执行放货动作
                    client.dropBox(f'drone_{drone}', land_ports[drone])
                    time.sleep(5)  # 等待放货完成
                    client.landAsync(vehicle_name = f'drone_{drone}')  # 控制无人机降落
                    time.sleep(5)  # 等待降落完成
                    cdb_client.rdb.delete(f'{proposal_id}:drone:{drone}')  # 删除redis中该无人机信息
                    cdb_client.rdb.delete(f'{proposal_id}:flight_plan:{drones[drone][3]}')  # 删除redis中该无人机信息
                    finish_que.append([drone, land_ports[drone]])  # 将[无人机id，终点机场名称]存入完成任务队列finish_que中
                    del drones_pos[drone]  # 删除无人机实时位置字典drones_pos中该无人机的信息
                    del drones[drone]  # 删除drones中该无人机的信息
                    del takeoff_ports[drone]  # 删除起飞机场字典takeoff_ports中该无人机的信息
                    que[land_ports[drone]].append(num)  # 将该无人机在终点机场中占用的位置空出
                    del land_ports[drone]  # 删除降落机场字典land_ports中该无人机的信息
                    drone_db.rdb.delete(f'{proposal_id}:drone_current:{drone}')  # 删除redis中该无人机的实时位置信息
                    break

            time.sleep(time_step)


def get_drone_pos():
    """获取每个无人机的位置，并将无人机位置信息存入redis"""
    global drones_pos, drones_id, drone_db, proposal_id, drones
    while True:  # 循环更新实时位置
        drones_pos_temp = drones_pos.copy()  # 复制无人机实时位置字典drones_pos，防止之后遍历过程中，有新无人机生成或完成任务的无人机被删除，导致drones_pos被修改报错
        for drone in drones_pos_temp:  # 遍历每个无人机的实时位置
            if drone not in drones_pos or drone not in drones:  # 如果该无人机已完成任务，相关信息被删除，则跳过
                continue
            if drones_pos[drone] and drones[drone][1]:  # 如果该无人机存在实时位置信息，且飞行任务仍在执行中
                # 将无人机的初始位置、实时位置、当前所处航路存入redis
                refresh_drone(drone_db, proposal_id, drone,
                              [initial_positions[drone].x_val, initial_positions[drone].y_val, initial_positions[drone].z_val],
                              drones_pos[drone], drones[drone][1][0])
        time.sleep(1)  # 更新频率


def AddDrones():  # 该功能可选，但是使用该功能会导致数据库飞行任务被修改，慎重使用，重新启动项目时需要将数据库恢复到启动前的状态
    """给完成飞行任务的无人机随机生成新的飞行任务"""
    global land_ports, ports_pos, finish_que, takeoff_ports
    from source.flight_plan.models import FlightRequirements
    from source.proposal.models import Proposals
    from source.uav.models import Drones
    from source.air_road.models import Airports
    import datetime

    proposal = Proposals.objects.get(name='proposal')  # 获取仿真方案proposal

    while True:
        ports_count = dict.fromkeys(ports_pos.keys(), 0)  # 定义字典，用于存储以每个机场为终点的无人机数量
        land_ports_copy = land_ports.copy()  # 复制land_posts，防止遍历过程中land_ports在其他地方被修改报错
        for land_drone in land_ports_copy:
            ports_count[land_ports_copy[land_drone]] += 1  # 计数，有多少无人机以该机场为终点
        if finish_que:  # if 队列中有已完成任务的无人机
            [finish_drone, finish_port] = finish_que.pop(0)  # 弹出一个已完成任务的无人机
            port_flag = False  # 标注是否为该无人机分配好新任务
            while not port_flag:
                for port in ports_count:  # 遍历所有机场
                    if ports_count[port] < 10 and port!=finish_port:  # 若以该机场为终点的无人机数量<10，且该机场不是该无人机当前所在的机场
                        land_ports[finish_drone] = port  # 更新该机场为该无人机的新任务的终点
                        port_flag = True
                        break
            takeoff_ports[finish_drone] = finish_port  # 设置该无人机的起飞机场为上一次任务的降落机场
            current_time = datetime.datetime.now()  # 读取当前时间
            drone_sample = Drones.objects.get(id=finish_drone)  # 在数据库中搜索该无人机
            takeoff_airport = Airports.objects.get(name=finish_port)  # 在数据库中搜索新任务的起飞机场
            land_airport = Airports.objects.get(name=land_ports[finish_drone])  # 在数据库中搜索新任务的降落机场
            flight_req_sample = FlightRequirements(proposal=proposal, name=f'drone_{finish_drone}_{current_time}',
                                                   drone=drone_sample, priority=1, start_airport=takeoff_airport,
                                                   end_airport=land_airport, type='0', end_time=current_time)
            flight_req_sample.save()  # 创建一个新的飞行任务
            print(f'new requirement has been created for drone_{finish_drone}')
            finish_num = que[takeoff_ports[finish_drone]].pop(0)  # 在起飞机场内给该无人机分配一个起飞位置
            # 更新新任务的出发点坐标到start_positions
            start_positions[finish_drone] = airsim.Vector3r(places[takeoff_ports[finish_drone]][finish_num][0],
                                                       places[takeoff_ports[finish_drone]][finish_num][1],
                                                       places[takeoff_ports[finish_drone]][finish_num][2])
            # 控制无人机起飞
            clients[finish_drone].takeoffAsync(vehicle_name=f'drone_{finish_drone}')
            time.sleep(5)  # 等待起飞完成
            # 启动无人机控制线程
            t_rerun = threading.Thread(target=run, args=[clients[finish_drone], finish_drone, finish_num])
            t_rerun.start()


if __name__ == "__main__":
    # listen线程，用于监听新的飞行任务、无人机等数据，并更新相关数据
    t_listen = threading.Thread(target=listen)
    t_listen.start()
    # 为完成飞行任务的无人机自动生成新任务的线程，该功能可选，但是使用该功能会导致数据库飞行任务被修改，慎重使用，重新启动项目时需要将数据库恢复到启动前的状态。恢复方式：启动项目之前备份db.sqlite3文件，重新启动项目之前用备份的db.sqlite3替换掉当前的db.sqlite3
    # t_adddrone = threading.Thread(target=AddDrones)
    # t_adddrone.start()
    # 位置更新线程，用于更新无人机的实时位置到redis
    t_pos = threading.Thread(target=get_drone_pos)
    t_pos.start()

    while True:
        try:
            drones_id_temp = drones.copy()  # 复制一份无人机信息，防止遍历过程中drones被修改导致报错
            for drone in drones_id_temp:  # 遍历每一个无人机
                if drones[drone] and (drone not in clients):  # 如果该无人机有未完成的飞行任务，但还未创建线程去控制该无人机执行飞行任务
                    # 为该无人机创建一个client连接到airsim模拟器
                    clients[drone] = airsim.MultirotorClient(IP)
                    clients[drone].confirmConnection()
                    while not que[takeoff_ports[drone]]:  # 如果该无人机的起飞机场已满，不存在空余位置
                        time.sleep(5)  # 等待直至起飞机场有空余位置出现
                    num = que[takeoff_ports[drone]].pop(0)  # 在该无人机的起始机场内，为该无人机分配一个空位置
                    # 将无人机分配到的初始位置存入initial_position字典中
                    initial_positions[drone] = airsim.Vector3r(places[takeoff_ports[drone]][num][0],
                                                               places[takeoff_ports[drone]][num][1],
                                                               places[takeoff_ports[drone]][num][2])
                    start_positions[drone] = initial_positions[drone]  # 当前飞行任务的出发位置，等于无人机的初始位置
                    # 设置无人机初始姿态
                    init_pose = airsim.Pose(position_val=initial_positions[drone],
                                            orientation_val=airsim.Quaternionr(0, 0, 0, 1))
                    # 在UE中创建无人机
                    clients[drone].simAddVehicle(f'drone_{drone}', 'simpleflight', pose=init_pose)
                    # 启动控制API，使无人机能够通过API进行控制
                    clients[drone].enableApiControl(True, vehicle_name=f'drone_{drone}')
                    # 解锁无人机
                    clients[drone].armDisarm(True, vehicle_name=f'drone_{drone}')
                    time.sleep(2)
                    # 控制无人机起飞
                    clients[drone].takeoffAsync(vehicle_name=f'drone_{drone}')
                    time.sleep(5)  # 等待起飞完成
                    # 启动一个无人机控制线程，传入参数有该无人机的client、无人机id、该无人机在起飞机场中分配到的位置
                    t_run = threading.Thread(target=run, args=[clients[drone], drone, num])
                    t_run.start()
            time.sleep(1)
        except Exception as e:
            print(e)
