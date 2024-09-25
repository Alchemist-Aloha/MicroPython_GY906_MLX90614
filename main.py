import time
from mlx90614 import *

scl_pin = 27
sda_pin = 26
sensor = MLX90614(1,scl_pin,sda_pin)

while True:
	print(sensor.ambient_temperature, sensor.object_temperature)
	time.sleep_ms(500)