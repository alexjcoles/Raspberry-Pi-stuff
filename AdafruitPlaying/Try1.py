# Import library and create instance of REST client.
from Adafruit_IO import Client

ADAFRUIT_IO_USERNAME = "Alexcoles"
ADAFRUIT_IO_KEY = "aio_rAAU81cu8zmKt5jYIgEvK0n5vCFg"


aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Send the value 100 to a feed called 'Foo'.
import time
import random

for i in range(10):
    random_number = random.randint(-10, 40)
    aio.send('welcome-feed', random_number)
    time.sleep(5)

# # Retrieve the most recent value from the feed 'Foo'.
# # Access the value by reading the `value` property on the returned Data object.
# # Note that all values retrieved from IO are strings so you might need to convert
# # them to an int or numeric type if you expect a number.
# data = aio.receive('Foo')
# print('Received value: {0}'.format(data.value))