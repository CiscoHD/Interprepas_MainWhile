import gpiozero as gpio
from time import sleep

sensor = gpio.DistanceSensor(echo=23, trigger=24)

try:
    while True:
        print(sensor.distance)
        sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    sensor.close()
