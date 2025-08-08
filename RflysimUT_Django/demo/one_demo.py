import airsim
import time

name = 'SimpleFlight'
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True, vehicle_name=name)
client.armDisarm(True, vehicle_name=name)

client.takeoffAsync()
time.sleep(5)
while True:
    client.moveToPositionAsync(1, 1, -124, 5, vehicle_name=name).join()
    client.moveToPositionAsync(23, 328, -124, 5, vehicle_name=name).join()
    client.moveToPositionAsync(231, 211, -124, 5, vehicle_name=name).join()
    client.moveToPositionAsync(190, -7, -124, 5, vehicle_name=name).join()
    client.moveToPositionAsync(1, 1, -124, 5, vehicle_name=name).join()
    client.moveToPositionAsync(1, 1, -5, 5, vehicle_name=name).join()
    time.sleep(10)


