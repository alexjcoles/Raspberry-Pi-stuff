from machine import I2C, Pin
import time

# SHT45 default address
SHT45_I2CADDR = 0x44

# Commands
SHT45_MEAS_HIGHREP_STRETCH = bytearray([0x2C, 0x06])

class SHT45:
    def __init__(self, i2c, addr=SHT45_I2CADDR):
        self.i2c = i2c
        self.addr = addr

    def measure(self):
        self.i2c.writeto(self.addr, SHT45_MEAS_HIGHREP_STRETCH)
        time.sleep_ms(500)
        data = self.i2c.readfrom(self.addr, 6)
        temp = data[0] << 8 | data[1]
        temp = -45 + (175 * temp / 65535)
        return temp

# Initialize I2C (SCL=Pin 5, SDA=Pin 4)
i2c = I2C(scl=Pin(5), sda=Pin(4))

# Initialize SHT45
sht45 = SHT45(i2c)

# Read temperature
temperature = sht45.measure()
print('Temperature: %f C' % temperature)
