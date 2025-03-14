import pygame as pg

pg.init()
fase = 50
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Control de puente móvil")   
clock = pg.time.Clock()
font = pg.font.Font(None, 36)

#coordenadas
bridgeParts = (((100,50,60,200), (650, 50, 60, 200)), ((80,250, 100, 60), (630, 250, 100, 60)), ((50, 310, 160, 30 ), (600, 310, 160, 30)))  
buttons = ((80, 450, 100, 100), (260, 450,100,100), (440, 450, 100, 100), (620, 450, 100, 100))
ilustrationDim = (0, 0, 800, 400)
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

#definirRectangulos
bridgeSupports = (pg.Rect(bridgeParts[0][0]), pg.Rect(bridgeParts[0][1]))
bridgeBase = (pg.Rect(bridgeParts[1][0]), pg.Rect(bridgeParts[1][1]))
bridgePillars = (pg.Rect(bridgeParts[2][0]), pg.Rect(bridgeParts[2][1]))
drawButtons = (pg.Rect(buttons[0]), pg.Rect(buttons[1]), pg.Rect(buttons[2]), pg.Rect(buttons[3]))
ilustration = pg.Rect(ilustrationDim)

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

printAll()
printPlatform(fase)
drawText("Bajando al " + str(100 - int(fase)) + "%", 300, 300, textColor)

pg.display.flip()
input("Presiona enter para continuar")
    