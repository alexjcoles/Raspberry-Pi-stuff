# Use https://github.com/CAATZ/Simple-Micropython-MLX90614-Library


import mlx90614
i2c = machine.I2C(0, sda=0, scl=1, freq=100000)
from machine import Pin, SoftI2C

# Create a SoftI2C bus on GPIO pins 4 and 5
# i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

# print("Scanning I2C bus...")
# devices = i2c.scan()
# print([hex(device) for device in devices])


sensor = mlx90614.MLX90614(i2c)
print(sensor.read_ambient_temp())
print(sensor.read_object_temp())

