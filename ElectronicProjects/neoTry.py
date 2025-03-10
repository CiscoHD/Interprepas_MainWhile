import board
import neopixel

LED_COUNT = 8       # Número de LEDs en la tira
PIN = board.D18     # GPIO 18

pixels = neopixel.NeoPixel(PIN, LED_COUNT, brightness=0.3, auto_write=False)

pixels.fill((255, 0, 0))  # Rojo
pixels.show()
