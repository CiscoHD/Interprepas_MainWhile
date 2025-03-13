import gpiozero as gpio
from time import sleep

sensor = gpio.DistanceSensor(echo=20, trigger=21)

try:
    while True:
        if sensor.distance > 0.09 and sensor.distance < 0.30:
            x = sensor.distance
            x *= 100
            porcentaje = (21-(30-x))*100/21
            print("porcentaje:", porcentaje)
        sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    sensor.close()
