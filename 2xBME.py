# List all the i2c devices by trying all the possible pins
import machine
from breakout_bme68x import BreakoutBME68X, STATUS_HEATER_STABLE
import time

# TODO this could take a list of device IDs rather than just one hard coded


def find_sensors(device_id, controller, sda_pin_number, scl_pin_number):
    print(f"About to scan with controller {controller} on SDA pin {sda_pin_number} and SCL pin {scl_pin_number}")
    sdaPIN = machine.Pin(sda_pin_number)
    sclPIN = machine.Pin(scl_pin_number)
    i2c = machine.I2C(controller, sda=sdaPIN, scl=sclPIN)
    devices_found = []

    devices = i2c.scan()
    if len(devices) != 0:
        print('  Number of I2C devices found =', len(devices))
        for device in devices:
            print("    Device Hexadecimal Address = ", hex(device))
            if device == device_id:
                print("    Found a device with the right ID")
                devices_found.append({"controller": controller, "sda": sda_pin_number, "scl": scl_pin_number})
    else:
        print("No I2C device found")

    return devices_found


# All the i2c interfaces on the Raspberry Pi Pico
# There's only 2 controllers but they can be on any of the pins
i2c_interfaces = [
                  {"controller": 0, "sda": 0, "scl": 1}, 
                  {"controller": 1, "sda": 2, "scl": 3},
                  {"controller": 0, "sda": 4, "scl": 5}, 
                  {"controller": 1, "sda": 6, "scl": 7},
                  {"controller": 0, "sda": 8, "scl": 9}, 
                  {"controller": 1, "sda": 10, "scl": 11},
                  {"controller": 0, "sda": 12, "scl": 13}, 
                  {"controller": 1, "sda": 14, "scl": 15},
                  {"controller": 0, "sda": 16, "scl": 17},
                  {"controller": 1, "sda": 18, "scl": 19},
                  {"controller": 0, "sda": 20, "scl": 21},
                  {"controller": 1, "sda": 26, "scl": 27},
                  ]
device_list = []
for interface in i2c_interfaces:
    new_ones = find_sensors(0x76, interface["controller"], interface["sda"], interface["scl"])
    print(new_ones)
    device_list.extend(new_ones)

print("Found devices of interest", device_list)

while True:
    for sensor in device_list:
        print(sensor)
        i2c = machine.I2C(sensor["controller"], sda=machine.Pin(sensor["sda"]), scl=machine.Pin(sensor["scl"]))
        bme = BreakoutBME68X(i2c)
        temperature, pressure, humidity, gas, status, _, _ = bme.read()
        heater = "Stable" if status & STATUS_HEATER_STABLE else "Unstable"
        print("Controller: {}, {:0.2f}c, {:0.2f}Pa, {:0.2f}%, {:0.2f} Ohms, Heater: {}".format(sensor["controller"], temperature, pressure, humidity, gas, heater))
        time.sleep(1.0)
