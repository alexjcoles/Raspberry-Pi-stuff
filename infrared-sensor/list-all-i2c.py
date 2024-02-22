# List all the i2c devices by trying all the possible pins
import machine


def list_i2c_devices(controller, sda_pin_number, scl_pin_number):
    print(f"About to scan with controller {controller} on SDA pin {sda_pin_number} and SCL pin {scl_pin_number}")
    sdaPIN = machine.Pin(sda_pin_number)
    sclPIN = machine.Pin(scl_pin_number)
    i2c = machine.I2C(controller, sda=sdaPIN, scl=sclPIN)

    devices = i2c.scan()
    if len(devices) != 0:
        print('  Number of I2C devices found =', len(devices))
        for device in devices:
            print("    Device Hexadecimal Address = ", hex(device))
    else:
        print("No I2C device found")


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

for interface in i2c_interfaces:
    list_i2c_devices(interface["controller"], interface["sda"], interface["scl"])


