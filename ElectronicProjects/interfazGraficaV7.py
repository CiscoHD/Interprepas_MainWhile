import pygame as pg
import gpiozero as gz
import time
import adafruit_pixelbuf
import board
from adafruit_raspberry_pi5_neopixel_write import neopixel_write
from adafruit_led_animation.animation.pulse import Pulse 

#Set up the GPIO pins
output1 = gz.OutputDevice(14)
output2 = gz.OutputDevice(15)
enable1 = gz.PWMOutputDevice(18)
enable2 = gz.PWMOutputDevice(13)
servo = gz.Servo(23, min_pulse_width=0.0005, max_pulse_width=0.0025)
upButton = gz.Button(2, pull_up=True)
downButton = gz.Button(3, pull_up=True)
distanceSensor = gz.DistanceSensor(echo=20, trigger=21)
NEOPIXEL = board.D12

#Set up the pygamen window
pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Control de puente móvil")
clock = pg.time.Clock()
font = pg.font.Font(None, 36)

#colores
bridgeColor = pg.Color(176,118,2)
borderBridgeColor = pg.Color(84,24,69)
borderButtonColor = pg.Color(122,122,122)
backColor = pg.Color(0,0,0)
moveColor = pg.Color(0,255,0)
forceColor = pg.Color(0,0,255)
stopColor = pg.Color(255,0,0)
ilustrationColor = pg.Color(0,200,255)
textColor = pg.Color(255,255,255)

#variables de control
statusPuente = "Paro_Emer"
running = True
mousePos = (0,0)
click = (0,0,0,0,0)
fase = 0
lectSensor = 0
minDistance = 9
maxDistance = 30
numPixels = 8

#coordenadas
bridgeParts = (((100,50,60,200), (650, 50, 60, 200)), ((80,250, 100, 60), (630, 250, 100, 60)), ((50, 310, 160, 30 ), (600, 310, 160, 30)))
buttons = ((80, 450, 100, 100), (260, 450,100,100), (440, 450, 100, 100), (620, 450, 100, 100))
ilustrationDim = (0, 0, 800, 400)
textos = (300,300)

#definirRectangulos
bridgeSupports = (pg.Rect(bridgeParts[0][0]), pg.Rect(bridgeParts[0][1]))
bridgeBase = (pg.Rect(bridgeParts[1][0]), pg.Rect(bridgeParts[1][1]))
bridgePillars = (pg.Rect(bridgeParts[2][0]), pg.Rect(bridgeParts[2][1]))
drawButtons = (pg.Rect(buttons[0]), pg.Rect(buttons[1]), pg.Rect(buttons[2]), pg.Rect(buttons[3]))
ilustration = pg.Rect(ilustrationDim)

# Removed redundant drawing calls outside the main loop

# Class for Raspberry Pi 5 usage
class Pi5Pixelbuf(adafruit_pixelbuf.PixelBuf):
    def __init__(self, pin, size, **kwargs):
        self._pin = pin
        super().__init__(size=size, **kwargs)
    def _transmit(self, buf):
        neopixel_write(self._pin, buf)

# LEDs init 
pixels = Pi5Pixelbuf(NEOPIXEL, numPixels, auto_write=True, byteorder="GRB")

# Animations init 
pulseAnima = Pulse(pixels,speed=.1, color=(255, 150, 0), period=1)

def ledUp():
    i = 0
    pixels.fill((0,0,0))
    for i in range(numPixels):
        pixels[i]=(255, 0, 0)
        time.sleep(.1)
        pixels.show()

def ledDown():
    pixels.fill((0, 0, 0))
    for i in reversed(range(numPixels)):
        pixels[i]=(255, 0, 0)
        time.sleep(.1)
        pixels.show()

def ledArrived_down():
    pixels.fill((0, 255, 0))
    pixels.show()

def ledArrived_up():
    pixels.fill((255, 0, 0))
    pixels.show()

def platformUp():
    enable1.value = 1
    enable2.value = .82
    output1.on()
    output2.off()

def stopPlatform():
    enable1.value = 0
    enable2.value = 0
    output1.off()
    output2.off()

def platformDown():
    enable1.value = 1
    enable2.value = .81
    output1.off()
    output2.on()

def openServo():
    servo.value = 0

def closeServo():
    servo.value = -1

def platformStatus(statusPuente):
    if upButton.is_pressed:
        return "Arriba"
    elif downButton.is_pressed:
        return "Abajo"
    else:
        return statusPuente

def printPlatform(fase):
    bridgePlatform = [160,60 + (1.7*(100-fase)), 490, 20]
    pg.draw.rect(screen, bridgeColor, bridgePlatform, 0)
    pg.draw.rect(screen, borderBridgeColor, bridgePlatform, 2)

def drawText (texto, x, y, color):
    varText = font.render(texto, True, color)
    screen.blit(varText, (x, y))

def printAll():
    pg.draw.rect(screen, ilustrationColor, ilustration, 0)
    pg.draw.rect(screen, bridgeColor, bridgeSupports[0], 0)
    pg.draw.rect(screen, borderBridgeColor, bridgeSupports[0], 2)
    pg.draw.rect(screen, bridgeColor, bridgeSupports[1], 0)
    pg.draw.rect(screen, borderBridgeColor, bridgeSupports[1], 2)
    pg.draw.rect(screen, bridgeColor, bridgeBase[0], 0)
    pg.draw.rect(screen, borderBridgeColor, bridgeBase[0], 2)
    pg.draw.rect(screen, bridgeColor, bridgeBase[1], 0)
    pg.draw.rect(screen, borderBridgeColor, bridgeBase[1], 2)
    pg.draw.rect(screen, bridgeColor, bridgePillars[0], 0)
    pg.draw.rect(screen, borderBridgeColor, bridgePillars[0], 2)
    pg.draw.rect(screen, bridgeColor, bridgePillars[1], 0)
    pg.draw.rect(screen, borderBridgeColor, bridgePillars[1], 2)
    pg.draw.rect(screen, moveColor, drawButtons[0], 0)
    pg.draw.rect(screen, borderButtonColor, drawButtons[0], 2)
    pg.draw.rect(screen, moveColor, drawButtons[1], 0)
    pg.draw.rect(screen, borderButtonColor, drawButtons[1], 2)
    pg.draw.rect(screen, forceColor, drawButtons[2], 0)
    pg.draw.rect(screen, borderButtonColor, drawButtons[2], 2)
    pg.draw.rect(screen, stopColor, drawButtons[3], 0)
    pg.draw.rect(screen, borderButtonColor, drawButtons[3], 2)
    pg.draw.polygon(screen, borderButtonColor, [(100, 520), (160, 520), (130, 480)])
    pg.draw.polygon(screen, borderButtonColor, [(280, 480), (340, 480), (310, 520)])
    drawText("Paro", 640, 480, textColor)
    drawText("emer", 640, 500, textColor)
    drawText("Forzar",450, 480, textColor)
    drawText("Bajada", 450, 500, textColor)

def stoppedPosition(statusPuente):
    if upButton.is_pressed or downButton.is_pressed:
        pg.Surface.fill(screen, backColor)
        printAll()
        stopPlatform()
    return platformStatus(statusPuente)

def distanceToPercentage(distance):
    distance *= 100
    percentage = ((maxDistance - minDistance) - (maxDistance - distance)) * 100 / (maxDistance - minDistance)
    return percentage

def buttonPress(mouseX, mouseY, button):
    if mouseX > button[0] and mouseX < button[0] + button[2]:
        if mouseY > button[1] and mouseY < button[1] + button[3]:
            return True
        else:
            return False
    else:
        return False

pixels.fill((0, 0, 0))
printAll()
try:
    while running == True:
        mousePos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()

        if statusPuente == "Abajo":
            ledArrived_down()
        elif statusPuente == "Arriba":
            ledArrived_up()
        elif statusPuente == "Subiendo":
            ledUp()
        elif statusPuente == "Bajando":
            ledDown()
        elif statusPuente == "Paro_Emer":
            pulseAnima.animate()

        if buttonPress(mousePos[0], mousePos[1], buttons[0]):
            if click[0] == 1 and statusPuente == "Abajo":
                platformUp()
                closeServo()
                statusPuente = "Subiendo"
                drawText("Puente subiendo al" + str(int(fase)) + "%", textos[0], textos[1], textColor)
                if upButton.is_pressed:
                    statusPuente = "Arriba"
                    stopPlatform()
                drawText("Puente subiendo al " + str(int(fase)) + "%", textos[0], textos[1], textColor)
                pg.time.wait(1000)
        elif buttonPress(mousePos[0], mousePos[1], buttons[1]):
            if click[0] == 1 and statusPuente == "Arriba":
                platformDown()
                statusPuente = "Bajando"
                drawText("Bajando al " + str((100 - int(fase))) + "%", textos[0], textos[1], textColor)
                if downButton.is_pressed:
                    statusPuente = "Abajo"
                    stopPlatform()
                drawText("Bajando al " + str(100 - int(fase)) + "%", textos[0], textos[1], textColor)
                pg.time.wait(1000)
        elif buttonPress(mousePos[0], mousePos[1], buttons[2]):
            if click[0] == 1 and statusPuente  == "Paro_Emer":
                platformDown()
                statusPuente = "Bajando"
                drawText("Bajando al " + str(100 - int(fase)) + "%", textos[0], textos[1], textColor)
        elif buttonPress(mousePos[0], mousePos[1], buttons[3]):
            if click[0]:
                stopPlatform()
                drawText("Paro Emer", textos[0], textos[1], textColor)
                statusPuente = "Paro_Emer"
        if statusPuente == "Abajo":
            openServo()
        lectSensor = distanceSensor.distance
        fase = distanceToPercentage(lectSensor)
        statusPuente = stoppedPosition(statusPuente)
        printAll()
        printPlatform(fase)
        drawText("Estado del puente: " + statusPuente, textos[0], textos[1], textColor)

        clock.tick(5)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
except KeyboardInterrupt:
    print("Programa finalizado por el usuario")
finally: 
    pixels.fill((0,0,0))
    pixels.show()
