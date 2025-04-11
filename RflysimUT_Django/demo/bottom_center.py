import airsim
import cv2
import numpy as np
import time

# 连接到AirSim
# client = airsim.MultirotorClient("127.0.0.1")
client = airsim.MultirotorClient("127.0.0.1")
client.confirmConnection()

# 初始化无人机
drone_name = "drone0"
# client.enableApiControl(True, drone_name)
# client.armDisarm(True, drone_name)

# 起飞
# client.takeoffAsync(vehicle_name=drone_name).join()

# # 设置飞行位置，以获得不同视角
# client.moveToPositionAsync(0, 0, -100, 5, vehicle_name=drone_name)

# 获取并显示图像的循环
try:
    while True:
        # 从无人机的前置摄像头获取图像
        responses = client.simGetImages([
            airsim.ImageRequest("bottom_center", airsim.ImageType.Scene, False, False)
        ], vehicle_name=drone_name)

        # 检查是否收到图像
        if responses:
            # 将图像数据转换为numpy数组
            img1d = np.frombuffer(responses[0].image_data_uint8, dtype=np.uint8)
            img_rgb = img1d.reshape(responses[0].height, responses[0].width, 3)

            # 显示图像
            cv2.namedWindow("Drone Camera View", cv2.WINDOW_NORMAL)
            # 设置窗口大小
            cv2.resizeWindow("Drone Camera View", 480, 320)

            cv2.imshow("Drone Camera View", img_rgb)

            # 按下 'q' 键退出循环
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("No image received")


        # 设置延迟，避免过快刷新
        time.sleep(0.01)
except Exception as e:
    pass
    # # 返航并降落
    # client.moveToPositionAsync(0, 0, -10, 5, vehicle_name=drone_name).join()
    # client.landAsync(vehicle_name=drone_name).join()
    # client.armDisarm(False, drone_name)
    # client.enableApiControl(False, drone_name)
    # cv2.destroyAllWindows()
