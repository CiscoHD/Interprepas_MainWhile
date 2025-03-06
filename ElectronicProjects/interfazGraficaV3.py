import pygame as pg
import gpiozero as gz

#Set up the GPIO pins
output1 = gz.OutputDevice(14)
output2 = gz.OutputDevice(15)
enable1 = gz.OutputDevice(18)
enable2 = gz.OutputDevice(13)
servo = gz.Servo(23, min_pulse_width=0.0005, max_pulse_width=0.0025)
upButton = gz.Button(2, pull_up=True)
downButton = gz.Button(3, pull_up=True)

#Set up the pygamen window
pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Control de puente móvil")   
clock = pg.time.Clock()
font = pg.font.Font(None, 36)

backColor = pg.Color(0,0,0)
upColor = pg.Color(0,255,0)
downColor = pg.Color(255,0,0)
ilustrationColor = pg.Color(0,200,255)
textColor = pg.Color(0,0,0)

statusPuente = "Abajo"
running = True
mousePos = (0,0)
click = (0,0,0,0,0)
ilustrationDim = (0,0,800,400)
buttons =((200,450,100,100), (500,450,100,100))

pg.draw.rect(screen, upColor, buttons[0], 0)
pg.draw.rect(screen, downColor, buttons[1], 0)
pg.draw.rect(screen, ilustrationColor, ilustrationDim, 0)

def platformUp():
    enable1.value = 1
    enable2.value = .6
    output1.on()
    output2.off()

def stopPlatform():
    enable1.value = 0
    enable2.value = 0
    output1.off()
    output2.off()

def platformDown():
    enable1.value = 1
    enable2.value = .6
    output1.off()
    output2.on()

def openServo():
    servo.value = 0

def closeServo():
    servo.value = -1

def platformStatus():
    if upButton.is_pressed:
        return "Arriba"
    elif downButton.is_pressed:
        return "Abajo"
    else:
        return "Moviendose"

def stoppedPosition():
    if upButton.is_pressed or downButton.is_pressed:
        pg.Surface.fill(screen, backColor)
        pg.draw.rect(screen, upColor, buttons[0], 0)
        pg.draw.rect(screen, downColor, buttons[1], 0)
        pg.draw.rect(screen, ilustrationColor, ilustrationDim, 0)
        stopPlatform()
    return platformStatus()
    

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

while running == True:
    mousePos = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()

    if buttonPress(mousePos[0], mousePos[1], buttons[0], statusPuente):
        if click[0] == 1 and statusPuente == "Abajo":
            platformUp()
            closeServo()
            statusPuente = "Moviendose"
            drawText("Subiendo", 350, 200, textColor)
    
    elif buttonPress(mousePos[0], mousePos[1], buttons[1], statusPuente):
        if click[0] == 1 and statusPuente == "Arriba":
            platformDown()
            statusPuente = "Moviendose"
            drawText("Bajando", 350, 200, textColor)
    pg.time.wait(3000)
    statusPuente = stoppedPosition()

    clock.tick(30)
    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()