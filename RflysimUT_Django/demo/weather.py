import airsim
import time

client = airsim.VehicleClient()
client.confirmConnection()

client.simEnableWeather(True)

time.sleep(5)
client.simSetWeatherParameter(airsim.WeatherParameter.RoadSnow, 1)
client.simSetWeatherParameter(airsim.WeatherParameter.Snow, 1)
time.sleep(5)

client.simSetWeatherParameter(airsim.WeatherParameter.RoadSnow, 0)
client.simSetWeatherParameter(airsim.WeatherParameter.Snow, 0)
time.sleep(2)
client.simSetWeatherParameter(airsim.WeatherParameter.Rain, 1)
client.simSetWeatherParameter(airsim.WeatherParameter.Roadwetness, 1)
time.sleep(5)

client.simSetWeatherParameter(airsim.WeatherParameter.Rain, 0)
client.simSetWeatherParameter(airsim.WeatherParameter.Roadwetness, 0)
time.sleep(2)
client.simSetWeatherParameter(airsim.WeatherParameter.Fog, 1)
time.sleep(5)

client.simEnableWeather(False)
