import pygame as pg
import gpiozero as gp 

pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Interfaz Grafica")
pg.font.init()
font = pg.font.Font(None, 36)
clock = pg.time.Clock()

#Definir colores
bridgeColor = pg.Color(176,118,2)
borderBridgeColor = pg.Color(84,24,69)
borderButtonColor = pg.Color(122,122,122)
backColor = pg.Color(0,0,0)
upColor = pg.Color(0,255,0)
downColor = pg.Color(255,0,0)
ilustrationColor = pg.Color(0,200,255)
textColor = pg.Color(255,255,255)

#Definir variables
running = True
fase = 0
statusPuente = "Detenido"
mousePos = (0,0)
i = 0

#definirDimensiones
bridgeParts = (((100,50,60,200), (650, 50, 60, 200)), ((80,250, 100, 60), (630, 250, 100, 60)), ((50, 310, 160, 30 ), (600, 310, 160, 30)))  
bridgePlatform = (160,60 + (60*fase), 490, 20)
buttons = ((200, 450, 100, 100), (500, 450,100,100))
ilustrationDim = (0, 0, 800, 400)

#definirRectangulos
bridgeSupports = (pg.Rect(bridgeParts[0][0]), pg.Rect(bridgeParts[0][1]))
bridgeBase = (pg.Rect(bridgeParts[1][0]), pg.Rect(bridgeParts[1][1]))
bridgePillars = (pg.Rect(bridgeParts[2][0]), pg.Rect(bridgeParts[2][1]))
upButton = pg.Rect(buttons[0])
downButton = pg.Rect(buttons[1])
ilustration = pg.Rect(ilustrationDim)

pg.Surface.fill(screen, backColor)
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
    pg.draw.rect(screen, upColor, upButton, 0)
    pg.draw.rect(screen, borderButtonColor, upButton, 2)
    pg.draw.rect(screen, downColor, downButton, 0)
    pg.draw.rect(screen, borderButtonColor, downButton, 2)


def drawText(texto, x, y, color):
    varText = font.render(texto, True, color)
    screen.blit(varText, (x, y))

def buttonPress(mouseX, mouseY, button, status):
    if mouseX > button[0] and mouseX < button[0] + button[2] and status == "Detenido":
        if mouseY > button[1] and mouseY < button[1] + button[3]:
            return True
        else:
            return False
    else:
        return False

def limpiarPantalla(tiempo, i, status):
    if i == tiempo:
        pg.Surface.fill(screen, backColor)
        pg.draw.rect(screen, upColor, upButton, 0)
        pg.draw.rect(screen, downColor, downButton, 0)
        pg.draw.rect(screen, ilustrationColor, ilustration, 0)
        #stop()
        i = 0
        status = "Detenido"
    return i, status

printAll()
printPlatform(fase)
while running:
    mousePos = pg.mouse.get_pos()
    click = pg.mouse.get_pressed(num_buttons = 5)
    if buttonPress(mousePos[0], mousePos[1], buttons[0], statusPuente):
        if click == (1,0,0,0,0):
            statusPuente = "Subida"
            drawText("Subiendo", 350, 550, textColor)
            i = 0

    elif buttonPress(mousePos[0], mousePos[1], buttons[1], statusPuente):
        if click == (1,0,0,0,0):
            statusPuente = "Bajada"
            drawText("Bajando", 350, 550, textColor)
            i = 0
    elif statusPuente == "Bajada":
        if fase < 3:
            fase += 1
            printAll()
            printPlatform(fase)
        else:
            fase = 0
    elif statusPuente == "Subida":
        if fase > 0:
            fase -= 1
            printAll()
            printPlatform(fase)
        else:
            fase = 3

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    pg.display.flip()
    i += 1
    i, statusPuente = limpiarPantalla(30, i, statusPuente)
    clock.tick(10)

pg.quit()