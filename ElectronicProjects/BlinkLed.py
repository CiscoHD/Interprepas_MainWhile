import gpiozero as gpio
import time 

led = gpio.LED(17)
def blinkLed():
    led.on()
    time.sleep(.5)
    led.off()
    time.sleep(.5)

while True:
    blinkLed()

