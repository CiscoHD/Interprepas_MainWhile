import pygame as pg
import gpiozero as gz

#Set up the GPIO pins
output1 = gz.OutputDevice(14)
output2 = gz.OutputDevice(15)
enable1 = gz.PWMOutputDevice(18)
enable2 = gz.PWMOutputDevice(13)
servo = gz.Servo(23, min_pulse_width=0.0005, max_pulse_width=0.0025)
upButton = gz.Button(2, pull_up=True)
downButton = gz.Button(3, pull_up=True)

#Set up the pygamen window
pg.init()
info = pg.display.Info()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Control de puente móvil")   
clock = pg.time.Clock()
font = pg.font.Font(None, 36)

#colores
bridgeColor = pg.Color(176,118,2)
borderBridgeColor = pg.Color(84,24,69)
borderButtonColor = pg.Color(122,122,122)
backColor = pg.Color(0,0,0)
upColor = pg.Color(0,255,0)
downColor = pg.Color(255,0,0)
ilustrationColor = pg.Color(0,200,255)
textColor = pg.Color(255,255,255)

#variables de control
statusPuente = "Abajo"
running = True
mousePos = (0,0)
click = (0,0,0,0,0)
fase = 0


#coordenadas
bridgeParts = (((100,50,60,200), (650, 50, 60, 200)), ((80,250, 100, 60), (630, 250, 100, 60)), ((50, 310, 160, 30 ), (600, 310, 160, 30)))  
bridgePlatform = (160,60 + (60*fase), 490, 20)
buttons = ((200, 450, 100, 100), (500, 450,100,100))
ilustrationDim = (0, 0, 800, 400)

#definirRectangulos
bridgeSupports = (pg.Rect(bridgeParts[0][0]), pg.Rect(bridgeParts[0][1]))
bridgeBase = (pg.Rect(bridgeParts[1][0]), pg.Rect(bridgeParts[1][1]))
bridgePillars = (pg.Rect(bridgeParts[2][0]), pg.Rect(bridgeParts[2][1]))
upButtonDraw = pg.Rect(buttons[0])
downButtonDraw = pg.Rect(buttons[1])
ilustration = pg.Rect(ilustrationDim)

pg.draw.rect(screen, upColor, buttons[0], 0)
pg.draw.rect(screen, downColor, buttons[1], 0)
pg.draw.rect(screen, ilustrationColor, ilustrationDim, 0)

def platformUp():
    enable1.value = 1
    enable2.value = .85
    output1.on()
    output2.off()

def stopPlatform():
    enable1.value = 0
    enable2.value = 0
    output1.off()
    output2.off()

def platformDown():
    enable1.value = 1
    enable2.value = .85
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
    bridgePlatform = (160,60 + (60*fase), 490, 20)
    pg.draw.rect(screen, bridgeColor, bridgePlatform, 0)
    pg.draw.rect(screen, borderBridgeColor, bridgePlatform, 2)

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
    pg.draw.rect(screen, upColor, upButtonDraw, 0)
    pg.draw.rect(screen, borderButtonColor, upButtonDraw, 2)
    pg.draw.rect(screen, downColor, downButtonDraw, 0)
    pg.draw.rect(screen, borderButtonColor, downButtonDraw, 2)

def stoppedPosition(statusPuente):
    if upButton.is_pressed or downButton.is_pressed:
        pg.Surface.fill(screen, backColor)
        printAll()
        stopPlatform()
    return platformStatus(statusPuente)

def buttonPress(mouseX, mouseY, button, status):
    if mouseX > button[0] and mouseX < button[0] + button[2] and (status == "Arriba" or status == "Abajo"):
        if mouseY > button[1] and mouseY < button[1] + button[3]:
            return True
        else:
            return False
    else:
        return False

def drawText (texto, x, y, color):
    varText = font.render(texto, True, color)
    screen.blit(varText, (x, y))

printAll()
while running == True:
    mousePos = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()

    if buttonPress(mousePos[0], mousePos[1], buttons[0], statusPuente):
        if click[0] == 1 and statusPuente == "Abajo":
            platformUp()
            closeServo()
            statusPuente = "Subiendo"
            if upButton.is_pressed:
                statusPuente = "Arriba"
                fase = 0
                stopPlatform()
            pg.time.wait(3000)
    
    elif buttonPress(mousePos[0], mousePos[1], buttons[1], statusPuente):
        if click[0] == 1 and statusPuente == "Arriba":
            platformDown()
            statusPuente = "Bajando"
            drawText("Bajando", 350, 200, textColor)
            if downButton.is_pressed:
                statusPuente = "Abajo"
                fase = 1
                stopPlatform()
            pg.time.wait(3000)
    if statusPuente == "Bajando":
        drawText("Bajando", 350, 500, textColor)
        if fase < 3:
            fase += 1
        else:
            fase = 0
    elif statusPuente == "Subiendo":
        drawText("Subiendo", 350, 200, textColor)
        if fase > 0:
            fase -= 1
        else:
            fase = 3
    if statusPuente == "Abajo":
        fase = 3
    elif statusPuente == "Arriba":
        fase = 0
    statusPuente = stoppedPosition(statusPuente)
    printAll()
    printPlatform(fase)

    clock.tick(5)
    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()
