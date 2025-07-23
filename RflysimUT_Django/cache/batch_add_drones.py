def batch_add_drones(num):
    """
    批量添加无人机功能，无人机自动命名为 “drone_” + 无人机id的形式，无人机id自动累加，不会覆盖已删除的无人机id
    参数num代表批量添加无人机的数量
    """
    try:
        import os
        import django
        # 设置环境变量，指向你的 Django 配置文件（例如 RflysimUT.settings）
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RflysimUT.settings")
        # 初始化 Django
        django.setup()
        from source.proposal.models import Proposals
        from source.uav.models import Drones
        proposal = Proposals.objects.get(name="proposal")
        for i in range(num):
            drones_sample = Drones.objects.create(proposal=proposal, max_speed=10, safe_radius=10)
            drones_sample.name = f"drone_{drones_sample.id}"
            drones_sample.save()
        print("批量添加无人机完成")
    except Exception as e:
        print("批量添加无人机失败", e)


# batch_add_drones(30)
