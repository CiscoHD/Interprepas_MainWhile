import pygame as pg
import gpiozero as gz

pg.init()
input1 = gz.DigitalOutputDevice(14)
input2 = gz.DigitalOutputDevice(15)
enable1 = gz.PWMOutputDevice(18) #Motor1
enable2 = gz.PWMOutputDevice(13) #Motor2'''

screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Controlador de puente")

backColor = pg.Color(0,0,0)
upColor = pg.Color(0,255,0)
downColor = pg.Color(255,0,0)
ilustrationColor = pg.Color(0,200,255)
textColor = pg.Color(0,0,0)

clock = pg.time.Clock()
font = pg.font.Font(None, 36)

i = 0
statusPuente = "Detenido"
running = True
buttons = ((200, 500), (450, 450), (100, 100), (100,100))
ilustrationDim = (0, 0, 800, 400)
mousePos = (0, 0)
click = (0, 0, 0, 0, 0)

upButton = pg.Rect(buttons[0][0], buttons[1][0], buttons[2][0], buttons[3][0])
downButton = pg.Rect(buttons[0][1], buttons[1][1], buttons[2][1], buttons[3][1])
ilustration = pg.Rect(ilustrationDim[0], ilustrationDim[1], ilustrationDim[2], ilustrationDim[3])

pg.draw.rect(screen, upColor, upButton, 0)
pg.draw.rect(screen, downColor, downButton, 0)
pg.draw.rect(screen, ilustrationColor, ilustration, 0)

def buttonPress(mouseX, mouseY, butX, butY, butW, butH, status):
    if mouseX > butX and mouseX < butX + butW and status == "Detenido":
        if mouseY > butY and mouseY < butY + butH :
            return True
        else:
            return False
    else:
        return False        

def drawText(texto, x, y, color):
    varText = font.render(texto, True, color)
    screen.blit(varText, (x, y))

def foward():
    input1.on()
    input2.off()
    enable1.value = 1
    enable2.value = .6

def backward(): 
    input1.off()
    input2.on()
    enable1.value = 1
    enable2.value = .6

def stop():
    input1.off()
    input2.off()
    enable1.value = 0
    enable2.value = 0

def limpiarPantalla(tiempo, i, status):
    if i == tiempo:
        pg.Surface.fill(screen, backColor)
        pg.draw.rect(screen, upColor, upButton, 0)
        pg.draw.rect(screen, downColor, downButton, 0)
        pg.draw.rect(screen, ilustrationColor, ilustration, 0)
        stop()
        i = 0
        status = "Detenido"
    return i, status

while running == True:
    mousePos = pg.mouse.get_pos()
    click = pg.mouse.get_pressed(num_buttons = 5)
    if buttonPress(mousePos[0], mousePos[1], buttons[0][0], buttons[1][0], buttons[2][0], buttons[3][0], statusPuente):
        if click == (1,0,0,0,0):
            statusPuente = "Subida"
            foward()
            drawText("Subiendo", 350, 100, textColor)
            i = 0

    elif buttonPress(mousePos[0], mousePos[1], buttons[0][1], buttons[1][1], buttons[2][1], buttons[3][1], statusPuente):
        if click == (1,0,0,0,0):
            statusPuente = "Bajada"
            backward()
            drawText("Bajando", 350, 100, textColor)
            i = 0

    pg.display.flip()
    i += 1
    i, statusPuente = limpiarPantalla(300, i, statusPuente)
    clock.tick(30)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()