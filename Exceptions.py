#погрешности
deltax0 = 4
deltay0 = 4
k = 4
deltax = deltax0
deltay = deltay0

#размер карты
MAP_WIDTH = 40
MAP_HEIGHT = 40

#размер стен по пикселям
WALL_WIDTH = 65
WALL_HEIGHT = 70

"""
Проверка, будет ли идти вверх
plX1, plY1, plX2, plY2 - координаты верхних углов персонажа пикселях
"""
def checkMoveUp(map, plC1, plC2):
    deltax = deltax0*k
    X1 = (plC1[0] + deltax) // WALL_WIDTH
    Y1 = (plC1[1] + deltay) // WALL_HEIGHT
    X2 = (plC2[0] - deltax) // WALL_WIDTH
    Y2 = (plC2[1] + deltay) // WALL_HEIGHT
    deltax = deltax0
    if (map.ourMap[Y1][X1] == 'b') or (map.ourMap[Y2][X2] == 'b') or (map.ourMap[Y1][X1] == 'c') or (map.ourMap[Y2][X2] == 'c'):
        return False
    else:
        return True

"""
Проверка, будет ли идти вниз
plC1,  plC2 - координаты нижних углов персонажа пикселях
"""
def checkMoveDown(map, plC1, plC2):
    deltax = deltax0 * k
    X1 = (plC1[0] + deltax) // WALL_WIDTH
    Y1 = (plC1[1] - deltay) // WALL_HEIGHT
    X2 = (plC2[0] - deltax) // WALL_WIDTH
    Y2 = (plC2[1] - deltay) // WALL_HEIGHT
    deltax = deltax0
    if (map.ourMap[Y1][X1] == 'b') or (map.ourMap[Y2][X2] == 'b') or (map.ourMap[Y1][X1] == 'c') or (map.ourMap[Y2][X2] == 'c'):
        return False
    else:
        return True

"""
Проверка, будет ли идти влево
plC1,  plC2 - координаты верхнего и нижнего углов персонажа пикселях
"""
def checkMoveLeft(map, plC1, plC2):
    deltay = deltay0 * k
    X1 = (plC1[0] + deltax) // WALL_WIDTH
    Y1 = (plC1[1] + deltay) // WALL_HEIGHT
    X2 = (plC2[0] + deltax) // WALL_WIDTH
    Y2 = (plC2[1] - deltay) // WALL_HEIGHT
    deltay = deltay0
    if (map.ourMap[Y1][X1] == 'b') or (map.ourMap[Y2][X2] == 'b') or (map.ourMap[Y1][X1] == 'c') or (map.ourMap[Y2][X2] == 'c'):
        return False
    else:
        return True


"""
Проверка, будет ли идти вправо
plC1,  plC2 - координаты верхнего и нижнего углов персонажа пикселях
"""
def checkMoveRight(map, plC1, plC2):
    deltay = deltay0 * k
    X1 = (plC1[0] - deltax) // WALL_WIDTH
    Y1 = (plC1[1] + deltay) // WALL_HEIGHT
    X2 = (plC2[0] - deltax) // WALL_WIDTH
    Y2 = (plC2[1] - deltay) // WALL_HEIGHT
    deltay = deltay0
    if (map.ourMap[Y1][X1] == 'b') or (map.ourMap[Y2][X2] == 'b') or (map.ourMap[Y1][X1] == 'c') or (map.ourMap[Y2][X2] == 'c'):
        return False
    else:
        return True

#Если пуля врезается, то она должна исчезнуть
def checkBoolet(map, bC):
    if (map.ourMap[bC[1] // WALL_HEIGHT][bC[0]//WALL_WIDTH] == 'b') or (map.ourMap[bC[1] // WALL_HEIGHT][bC[0]//WALL_WIDTH] == 'c'):
        return True
    else:
        return False