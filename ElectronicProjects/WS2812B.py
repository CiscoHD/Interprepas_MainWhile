import board
import neopixel
import time

LED_COUNT = 8
PIN = board.D18
pixels = neopixel.NeoPixel(PIN, LED_COUNT, brightness=0.5, auto_write=False)

def wheel(pos):
    """Convierte un valor de 0-255 en un color RGB."""
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(LED_COUNT):
            pixels[i] = wheel((i * 256 // LED_COUNT + j) & 255)
        pixels.show()
        time.sleep(wait)

while True:
    rainbow_cycle(0.05)

