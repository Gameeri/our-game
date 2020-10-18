"""
Функция создания карты со случайным генератором стенок
"""


def createMap(N, M, lBMin, lBMax, cB):
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
    return ourMap


"""
Конструктор карты
"""


class Map(object):
    def __init__(self, N, M):
        self.N = N
        self.M = M
        lBMin = 7
        lBMax = 20
        cB = 15
        self.ourMap = createMap(N, M, lBMin, lBMax, cB)

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
