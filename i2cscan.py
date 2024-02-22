from machine import Pin, I2C

# configure I2C
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)  # Change the parameters as per your connection

print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))

  for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))