"""
Функция создания карты со случайным генератором стенок
"""
#размер карты
MAP_WIDTH = 20
MAP_HEIGHT = 20

#размер стен по пикселям
WALL_WIDTH = 65
WALL_HEIGHT = 70

#размер вещей по пикселям
ITEM_WIDTH = 65
ITEM_HEIGHT = 70

#размер карты в пикселях
total_level_width  = MAP_WIDTH*WALL_WIDTH # Высчитываем фактическую ширину уровня
total_level_height = MAP_HEIGHT*WALL_HEIGHT   # высоту


def createMap(N, M, lBMin, lBMax, cB, cI):

    #Основная часть заполнения карты стенками
    ourMap = ['e'] * N
    for i in range(N):
        ourMap[i] = ['e'] * M
    import random
    for _ in range(cB):
        x = random.randrange(0, M - 1, 1)
        y = random.randrange(0, N - 1, 1)
        while (ourMap[y][x] != 'e'):
            x = random.randrange(0, M - 1, 1)
            y = random.randrange(0, N - 1, 1)
        side = random.randrange(0, 3, 1)
        if (side == 0):
            for i in range(random.randrange(lBMin, lBMax, 1)):
                if ((y - i < 0) & (ourMap[y][x] != 'e')):
                    break
                ourMap[y - i][x] = 'b'
        if (side == 1):
            for i in range(random.randrange(lBMin, lBMax, 1)):
                if ((x + i >= M) & (ourMap[y][x] != 'e')):
                    break
                ourMap[y][x + i] = 'b'
        if (side == 2):
            for i in range(random.randrange(lBMin, lBMax, 1)):
                if ((y + i >= N) & (ourMap[y][x] != 'e')):
                    break
                ourMap[y + i][x] = 'b'
        if (side == 3):
            for i in range(random.randrange(lBMin, lBMax, 1)):
                if ((y + i >= N) & (ourMap[y][x] != 'e')):
                    break
                ourMap[y + i][x] = 'b'

    #Стенки по границам
    for i in range(N):
        if (i == 0) or (i == N-1):
            for j in range(M):
                ourMap[i][j] = 'b'
        else:
            ourMap[i][0] = 'b'
            ourMap[i][M-1] = 'b'

    #освобождаем серединку
    for i in range(N//2 - 1, N//2 + 2):
        for j in range(M//2 - 1, M//2 + 2):
            ourMap[i][j] = 'e'

    for _ in range(cB//6):
        i = random.randrange(1, N-1, 1)
        for j in range(1, M-1):
            ourMap[i][j] = 'e'

    for _ in range(cI):
        x = random.randrange(1, M - 2, 1)
        y = random.randrange(1, N - 2, 1)
        while (ourMap[y][x] != 'e'):
            x = random.randrange(1, M - 2, 1)
            y = random.randrange(1, N - 2, 1)
        ourMap[y][x] = 't'
    x = random.randrange(1, M - 2, 1)
    y = random.randrange(0, N - 2, N - 2)
    ourMap[y][x] = 'c'
    x = random.randrange(0, M - 2, M - 2)
    y = random.randrange(1, N - 2, 1)
    ourMap[y][x] = 'c'
    return ourMap


"""
Конструктор карты
"""


class Map(object):
    def __init__(self, N, M):
        self.N = N
        self.M = M
        lBMin = 7
        lBMax = 10
        cB = 15
        cI = 15
        self.ourMap = createMap(N, M, lBMin, lBMax, cB, cI)

    """
    Функция, которая проверяет, что находится в клетке
    Возвращает:
    'b' - стенка
    'e' - пусто
    't' - ямка, где будут вещи
    """

    def checkCell(self, x, y):
        return self.ourMap[y][x]

    """
    Печать карты(для себя)
    """

    def printMap(self):
        for i in range(self.N):
            s = ''
            for j in range(self.M):
                s += str(self.ourMap[i][j]) + ' '
            print(s)

#наша карта
MAP = Map(MAP_WIDTH, MAP_HEIGHT)
