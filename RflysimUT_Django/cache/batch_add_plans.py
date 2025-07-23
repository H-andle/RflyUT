def get_airports_from_db():
    """
    获取数据库中所有机场数据，两个返回值为机场id列表、以机场id为 key机场数据类为value的字典
    """
    import os
    import django
    # 设置环境变量，指向你的 Django 配置文件（例如 RflysimUT.settings）
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RflysimUT.settings")
    # 初始化 Django
    django.setup()
    from source.air_road.models import Airports
    airports = Airports.objects.all()
    airports_id_list = []
    airports_class_dict = {}
    for airport in airports:
        airports_id_list = airports_id_list + [airport.id]
        airports_class_dict[airport.id] = airport
    return airports_id_list, airports_class_dict


# airports_id_list, airports_class_dict = get_airports_from_db()
# print(airports_id_list)
# print(airports_class_dict)


def add_a_plan(drone_id, start_airport_name, end_airport_name):
    """添加一个飞行计划,输入参数为无人机id、起飞机场名称，降落机场名称"""
    import os
    import django
    # 设置环境变量，指向你的 Django 配置文件（例如 RflysimUT.settings）
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RflysimUT.settings")
    # 初始化 Django
    django.setup()
    from source.proposal.models import Proposals
    from source.uav.models import Drones
    proposal = Proposals.objects.get(name="proposal")  # 获取proposal类

    # # 添加一个无人机,名称为drone_{无人机id}，例如drone_1,drone_2......
    # drones_sample = Drones.objects.create(proposal=proposal, max_speed=10, safe_radius=10)  # 实例化一个无人机类
    # drones_sample.name = f"drone_{drones_sample.id}"  # 修改该无人机类的名称为drone_{无人机id}
    # drones_sample.save()  # 保存该无人机类到数据库，添加无人机成功
    drones_sample = Drones.objects.get(id=drone_id)

    # 为该无人机添加一个飞行计划，假设该无人机起飞机场id为1，降落机场id为2
    from source.flight_plan.models import FlightRequirements
    from source.air_road.models import Airports
    from datetime import datetime
    start_airport = Airports.objects.get(name=start_airport_name)  # 根据id获取起飞机场数据类
    end_airport = Airports.objects.get(name=end_airport_name)  # 根据id获取降落机场数据类
    flight_requirement_sample = FlightRequirements.objects.create(
        proposal=proposal, name=drones_sample.name, drone=drones_sample,
        start_airport=start_airport, end_airport=end_airport,
        end_time=datetime.now()
    )  # 创建一个飞行计划，起飞机场id为1，降落机场id为2，无人机为刚创建的drone_sample，名称与无人机同名


# 通过循环调用add_a_plan实现批量添加飞行计划的功能
# for i in range(1, 6):
#     add_a_plan(i, '(-335,-23)', '(-444,-217)')

