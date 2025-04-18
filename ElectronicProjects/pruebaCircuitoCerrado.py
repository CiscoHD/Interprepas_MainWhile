factor1 = 0.9
factor2 = 0.8 
max_height = 600
min_height = 200

def upPlatform(y1, y2):
    y1 += factor1
    y2 += factor2
    return y1, y2

def downPlatform(y1, y2):
    y1 -= factor1
    y2 -= factor2
    return y1, y2

def checkPlatform(y1, y2, factor1, factor2):
    if y1 > y2:
        factor2 += 0.01
    if y1 < y2:
        factor1 += 0.01
    return factor1, factor2

def stopPlatform(y1, y2):
    factor1 = 0
    factor2 = 0
    return factor1, factor2

contador = 0
print("Control de la plataforma")
y1, y2 = min_height, min_height

button = '0';
while button != '4':
    if button == '1':
        y1, y2 = upPlatform(y1, y2)
    if button == '2':
        y1, y2 = downPlatform(y1, y2)
    if button == '3':
        y1, y2 = stopPlatform(y1, y2)
    
    factor1, factor2 = checkPlatform(y1, y2, factor1, factor2)
    if contador == 0:
        print(f"Plataforma en posición: {y1}, {y2}")
        button = input("Presione 1 para subir, 2 para bajar, 3 para detener, 4 para salir: ")
        contador = 50
    contador -= 1