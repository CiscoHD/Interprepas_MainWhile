import gpiozero as gpio
from time import sleep

sensor = gpio.DistanceSensor(echo=23, trigger=24)

try:
    while True:
        if sensor.distance > 0.09 and sensor.distance < 0.30:
            x = sensor.distance7
            x *= 100
            porcentaje = (21-(30-x))*100/21
            print("porcentaje:", porcentaje)
        sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    sensor.close()
