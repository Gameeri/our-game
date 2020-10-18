import pygame
import random
from os import path
from Map import *
from Wall import *
from Bullet import *

player_stand = pygame.image.load('ded3.png')
player_right = pygame.image.load('ded_right2.png')
player_left = pygame.image.load('ded_left2.png')
player_up = pygame.image.load('ded_up2.png')
player_stand = pygame.transform.scale(player_stand, (60,55))
player_right = pygame.transform.scale(player_right, (60,55))
player_left = pygame.transform.scale(player_left, (60,55))
player_up = pygame.transform.scale(player_up, (60,55))

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

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_stand
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedx = 0
        self.speedy = 0
        self.left, self.right, self.up, self.down = 0, 0, 0, 1


    def update(self):
        self.speedx = 0
        self.speedy = 0
        # управление игроком
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -8
            self.image = player_left
            self.left, self.right, self.up, self.down = 1, 0, 0, 0
        elif keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 8
            self.left, self.right, self.up, self.down = 0, 1, 0, 0

        elif keystate[pygame.K_UP] or keystate[pygame.K_w]:
            self.speedy = -8
            self.left, self.right, self.up, self.down = 0, 0, 1, 0
        elif keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            self.speedy = 8
            self.left, self.right, self.up, self.down = 0, 0, 0, 1

        if self.right == 1:
            self.image = player_right
        elif self.left == 1:
            self.image = player_left
        elif self.up == 1:
            self.image = player_up
        elif self.down == 1:
            self.image = player_stand
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        if(self.left == 1):
            bullet.direction = 'LEFT'
        elif (self.right == 1):
            bullet.direction = 'RIGHT'
        elif (self.up == 1):
            bullet.direction = 'UP'
        elif (self.down == 1):
            bullet.direction = 'DOWN'
        all_sprites.add(bullet)
        bullets.add(bullet)

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
bullets = pygame.sprite.Group()
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
            if event.key == pygame.K_SPACE:
                player.shoot()

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