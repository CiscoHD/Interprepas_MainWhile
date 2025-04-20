import time

import adafruit_pixelbuf
import board
from adafruit_raspberry_pi5_neopixel_write import neopixel_write
from  adafruit_led_animation.animation.pulse import Pulse
NEOPIXEL = board.D12
num_pixels = 8

class Pi5Pixelbuf(adafruit_pixelbuf.PixelBuf):
    def __init__(self, pin, size, **kwargs):
        self._pin = pin
        super().__init__(size=size, **kwargs)

    def _transmit(self, buf):
        neopixel_write(self._pin, buf)

pixels = Pi5Pixelbuf(NEOPIXEL, num_pixels, auto_write=True, byteorder="BGR")

animation = Pulse(pixels, speed=0.01, color= (255, 0, 0), period=1)

try:
    while True:
        animation.animate()
finally:
    time.sleep(.02)
    pixels.fill(0)
    pixels.show()
