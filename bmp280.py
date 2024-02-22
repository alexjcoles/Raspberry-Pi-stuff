import time
from breakout_bmp280 import BreakoutBMP280
from pimoroni_i2c import PimoroniI2C
import machine


i2c = machine.I2C(0, sda=12, scl=13)
bmp = BreakoutBMP280(i2c)

while True:
    reading = bmp.read()
    print(reading)
    time.sleep(1.0)
