import pygame
import random
from os import path
from Map import *
from Wall import *
from Bullet import *
from pygame.math import Vector2

#картинки
player_stand = pygame.image.load('ded3.png')
player_right = pygame.image.load('ded_right2.png')
player_left = pygame.image.load('ded_left2.png')
player_up = pygame.image.load('ded_up2.png')
player_stand = pygame.transform.scale(player_stand, (60,55))
player_right = pygame.transform.scale(player_right, (60,55))
player_left = pygame.transform.scale(player_left, (60,55))
player_up = pygame.transform.scale(player_up, (60,55))

#размер карты
MAP_WIDTH = 20
MAP_HEIGHT = 20

#размер стен по пикселям
WALL_WIDTH = 65
WALL_HEIGHT = 70

#размер карты в пикселях
total_level_width  = MAP_WIDTH*WALL_WIDTH # Высчитываем фактическую ширину уровня
total_level_height = MAP_HEIGHT*WALL_HEIGHT   # высоту

#наша карта
MAP = Map(MAP_WIDTH, MAP_HEIGHT)

#размер экрана
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
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_stand
        self.rect = self.image.get_rect()
        self.rect.center = Vector2(pos)
        self.speed = Vector2(0,0)
        self.left, self.right, self.up, self.down = 0, 0, 0, 1
        self.vel = 8 #величина скорости

    def update(self):
        self.speed = Vector2(0,0)
        # управление игроком
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speed.x = -self.vel
            self.image = player_left
            self.left, self.right, self.up, self.down = 1, 0, 0, 0
        elif keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speed.x = self.vel
            self.image = player_right
            self.left, self.right, self.up, self.down = 0, 1, 0, 0

        elif keystate[pygame.K_UP] or keystate[pygame.K_w]:
            self.speed.y = -self.vel
            self.image = player_up
            self.left, self.right, self.up, self.down = 0, 0, 1, 0
        elif keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            self.speed.y = self.vel
            self.image = player_stand
            self.left, self.right, self.up, self.down = 0, 0, 0, 1


        if self.rect.right > total_level_width:
            self.rect.right = total_level_width
        elif self.rect.left < 0:
            self.rect.left = 0
        else:
            self.rect.x += self.speed.x

        if self.rect.bottom > total_level_height:
            self.rect.bottom = total_level_height
        elif self.rect.top < 0:
            self.rect.top = 0
        else:
            self.rect.y += self.speed.y

    def shoot(self):
        bullet = Bullet(self.rect.center)
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
        shoot_sound.play()

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
player = Player((total_level_width/2, total_level_height/2))
camera = Vector2(total_level_width/2, total_level_height/2)
all_sprites.add(player)
platforms = []
# счетчик
score = 0

#отображение стен
coord = Vector2(0,0) # координаты
for row in MAP.ourMap: # вся строка
    for col in row: # каждый символ
        if col == "b":
            pf = Platform(coord)
            all_sprites.add(pf)
            platforms.append(pf)
        if col == "t":
            m = Item()
            all_sprites.add(m)
            items.add(m)

        coord.x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
    coord.y += PLATFORM_HEIGHT    #то же самое и с высотой
    coord.x = 0                   #на каждой новой строчке начинаем с нуля

shoot_sound = pygame.mixer.Sound('shooti1.wav')
shoot_sound.set_volume(0.03)
pygame.mixer.music.load('CrushingEnemies.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(loops=-1)

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

    heading = player.rect.center - camera
    camera += heading * 0.1
    offset = -camera + Vector2(WIDTH//2, HEIGHT//2)

    # Рендеринг
    #screen.fill(GREEN)
    screen.blit(background, background_rect)
    #all_sprites.draw(screen)
    #screen.blit(player.image, player.rect.topleft + offset)
    for s in all_sprites:
        screen.blit(s.image, s.rect.topleft + offset)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()