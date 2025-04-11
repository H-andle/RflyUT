import airsim
import numpy as np
import cv2
import time

# 连接到AirSim
client = airsim.MultirotorClient()
client.confirmConnection()

# 初始化无人机
drone_name = "drone0"
client.enableApiControl(True, drone_name)
client.armDisarm(True, drone_name)

# 起飞
# client.takeoffAsync(vehicle_name=drone_name).join()

# # 设置飞行位置（确保激光雷达可以扫描到物体）
# client.moveToPositionAsync(0, 0, -100, 5, vehicle_name=drone_name)
#
# # 初始化显示窗口
# cv2.namedWindow("LiDAR Scan", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("LiDAR Scan", 800, 800)

try:
    while True:
        # 获取激光雷达数据
        lidar_data = client.getLidarData(lidar_name="LidarSensor1", vehicle_name=drone_name)

        if len(lidar_data.point_cloud) > 0:
            # 将点云数据转换为 (x, y, z) 点的列表
            points = np.array(list(zip(*(iter(lidar_data.point_cloud),) * 3)))
            x, y, z = points[:, 0], points[:, 1], points[:, 2]

            # 转换为2D平面坐标系
            lidar_image = np.zeros((800, 800, 3), dtype=np.uint8)
            scale = 5  # 缩放因子
            center = 400  # 图像中心位置

            for i in range(len(x)):
                px = int(center + x[i] * scale)
                py = int(center - y[i] * scale)

                # 检查点是否在画布范围内
                if 0 <= px < 800 and 0 <= py < 800:
                    lidar_image[py, px] = (255, 255, 255)  # 将点绘制为白色

            # 显示图像
            cv2.imshow("LiDAR Scan", lidar_image)

            # 按下 'q' 键退出循环
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("No LiDAR data received")
        time.sleep(0.1)

except Exception as e:
    print(e)
    pass
    # # 返航并降落
    # client.moveToPositionAsync(0, 0, -10, 5, vehicle_name=drone_name).join()
    # client.landAsync(vehicle_name=drone_name).join()
    # client.armDisarm(False, drone_name)
    # client.enableApiControl(False, drone_name)
    # cv2.destroyAllWindows()