import pygame
import random
from os import path
from Map import *
from Wall import *
from Player import *

MAP = Map(10,10)

WIDTH = 650
HEIGHT = 700
FPS = 30

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Item(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((65,70))
        self.image.fill(RED)
        self.rect = self.image.get_rect()


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
#графика
background = pygame.image.load(path.join('BG.png')).convert()
background_rect = background.get_rect()

all_sprites = pygame.sprite.Group()
items = pygame.sprite.Group()
player = Player(WIDTH//2, HEIGHT//2)
all_sprites.add(player)
platforms = []
# счетчик
score = 0

#отображение стен
x=y=0 # координаты
for row in MAP.ourMap: # вся строка
    for col in row: # каждый символ
        if col == "e":
            pf = Platform(x,y)
            all_sprites.add(pf)
            platforms.append(pf)
        if col == "t":
            m = Item()
            all_sprites.add(m)
            items.add(m)

        x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
    y += PLATFORM_HEIGHT    #то же самое и с высотой
    x = 0                   #на каждой новой строчке начинаем с нуля

# вывод текста на экран
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)

    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if (pygame.sprite.spritecollide(player, items, True)):
                    score += 1

    # Обновление
    all_sprites.update()
    # Рендеринг
    screen.fill(GREEN)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 30, WIDTH / 2, 10)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()