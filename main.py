import random
from Weapon import *
from Item import *
from pygame.math import Vector2
from os import path
import pygame_menu
from pygame_menu import sound
import time

snd_dir = path.join(path.dirname(__file__), 'sounds')
img_dir = path.join(path.dirname(__file__), 'image')

#картинки
player_stand = pygame.image.load(path.join(img_dir,'ded3.png'))
player_right = pygame.image.load(path.join(img_dir,'ded_right2.png'))
player_left = pygame.image.load(path.join(img_dir,'ded_left2.png'))
player_up = pygame.image.load(path.join(img_dir,'ded_up2.png'))
player_stand = pygame.transform.scale(player_stand, (64,59))
player_right = pygame.transform.scale(player_right, (60,55))
player_left = pygame.transform.scale(player_left, (60,55))
player_up = pygame.transform.scale(player_up, (60,55))
tomato2 = pygame.image.load(path.join(img_dir,'tomato.png'))
tomato2 = pygame.transform.scale(tomato2, (30,30))
gun = pygame.image.load(path.join(img_dir,'Gun.png'))
gun = pygame.transform.scale(gun, (30,30))

#размер карты
MAP_WIDTH = 40
MAP_HEIGHT =40

#размер стен по пикселям
WALL_WIDTH = 65
WALL_HEIGHT = 70

#размер вещей по пикселям
ITEM_WIDTH = 65
ITEM_HEIGHT = 70

#размер карты в пикселях
total_level_width  = MAP_WIDTH*WALL_WIDTH # Высчитываем фактическую ширину уровня
total_level_height = MAP_HEIGHT*WALL_HEIGHT   # высоту

#размер экрана
WIDTH = 650
HEIGHT = 500
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
        self.coin = 0
        self.Weap = Dynamite
        self.gun = False

    def update(self):
        self.speed = Vector2(0,0)
        # управление игроком
        keystate = pygame.key.get_pressed()
        if (keystate[pygame.K_LEFT] or keystate[pygame.K_a]) and checkMoveLeft(MAP, player.rect.topleft, player.rect.bottomleft):
            self.speed.x = -self.vel
            self.image = player_left
            self.left, self.right, self.up, self.down = 1, 0, 0, 0
        elif (keystate[pygame.K_RIGHT] or keystate[pygame.K_d]) and checkMoveRight(MAP, player.rect.topright, player.rect.bottomright):
            self.speed.x = self.vel
            self.image = player_right
            self.left, self.right, self.up, self.down = 0, 1, 0, 0

        elif (keystate[pygame.K_UP] or keystate[pygame.K_w]) and checkMoveUp(MAP, player.rect.topleft, player.rect.topright):
            self.speed.y = -self.vel
            self.image = player_up
            self.left, self.right, self.up, self.down = 0, 0, 1, 0
        elif (keystate[pygame.K_DOWN] or keystate[pygame.K_s]) and checkMoveDown(MAP, player.rect.bottomleft, player.rect.bottomright):
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
        bullet = self.Weap(self.rect.center)
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

class Dynamite(Weapon):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = bul
        self.rect = self.image.get_rect()
        self.vel = 2
        self.rect.center = pos
    def update(self):
        super().update()


# Создаем игру и окно
pygame.init()
pygame.mixer.init()

shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'shooti1.wav'))
shoot_sound.set_volume(0.08)

#добавление спрайтов
all_sprites = pygame.sprite.Group()
items = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player((total_level_width//2, total_level_height//2))


platforms = pygame.sprite.Group()
# счетчик


#отображение стен
coord = Vector2(0,0) # координаты
i = 0
for row in MAP.ourMap: # вся строка
    #это для определения координат пули
    j = 0
    for col in row: # каждый символ
        if col == "b":
            pf = Platform(coord)
            all_sprites.add(pf)
            platforms.add(pf)
        if col == "t":
            #и тут передал координаты
            m = Item(Vector2(j * ITEM_WIDTH, i * ITEM_HEIGHT))
            all_sprites.add(m)
            items.add(m)
        #а это тоже для координат
        j += 1
        coord.x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
    coord.y += PLATFORM_HEIGHT    #то же самое и с высотой
    coord.x = 0                   #на каждой новой строчке начинаем с нуля
    i += 1
all_sprites.add(player)

#отображение текста
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Цикл игры


def set_difficulty(value, difficulty):
    # Do the job here !
    pass


def start_the_game():
    time.sleep(0.2)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()
    # графика
    background = pygame.image.load(path.join(img_dir, 'BG.png')).convert()
    background_rect = background.get_rect()

    # звуки

    pygame.mixer.music.load(path.join(snd_dir, 'CrushingEnemies.mp3'))
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(loops=-1)
    chest_sound = pygame.mixer.Sound(path.join(snd_dir, 'coin1.wav'))
    chest_sound.set_volume(0.05)
    gun_sound = pygame.mixer.Sound(path.join(snd_dir, 'gun.wav'))
    gun_sound.set_volume(0.3)
    tomato_sound = pygame.mixer.Sound(path.join(snd_dir, 'tomato.wav'))
    tomato_sound.set_volume(0.3)

    score = 0
    running = True
    camera = Vector2(total_level_width // 2, total_level_height // 2)
    while running:
        # Держим цикл на правильной скорости
        clock.tick(FPS)

        # Ввод процесса (события)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:

                    if (pygame.sprite.spritecollide(player, items, True)):
                        n = random.randint(0,4) #рандомное целое на отрезке. для вероятности.
                        if n != 4:
                            score += 1
                            chest_sound.play()
                        else:
                            player.Weap = Gun
                            gun_sound.play()
                            player.gun = True
                if event.key == pygame.K_SPACE:
                    player.shoot()
                if event.key == pygame.K_r:
                    if player.gun == True:
                        if(player.Weap == Gun):
                            player.Weap = Tomato
                            tomato_sound.play()
                        else:
                            player.Weap = Gun
                            gun_sound.play()



        # Обновление
        all_sprites.update()
        if(player.Weap == Dynamite):
            pygame.sprite.groupcollide(platforms, bullets, True, True)
        #движение карты
        heading = player.rect.center - camera
        camera += heading*0.1
        offset = camera - Vector2(WIDTH // 2, HEIGHT // 2)
        X = MAP_WIDTH*WALL_WIDTH - WIDTH
        Y = MAP_HEIGHT*WALL_HEIGHT - HEIGHT

        if offset.x < 0:
            offset.x = 0
        if offset.x > X :
            offset.x = X

        if offset.y < 0:
            offset.y = 0
        if offset.y > Y:
            offset.y = Y

        # Рендеринг
        screen.blit(background, background_rect)

        for s in all_sprites:
            screen.blit(s.image, s.rect.topleft - offset)

        draw_text(screen, str(score), 18, WIDTH / 2, 10)
        if player.Weap == Tomato:
            screen.blit(tomato2, Vector2(20,20))
        elif player.Weap == Gun:
            screen.blit(gun, Vector2(20, 20))
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()

surface = pygame.display.set_mode((650, 500))
bkgr = pygame.image.load(path.join('main.jpg')).convert()
menu = pygame_menu.Menu(300, 400, 'Hello, friend',
                       theme=pygame_menu.themes.THEME_GREEN)
surface.blit(bkgr, bkgr.get_rect())
menu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

engine = sound.Sound()
engine.set_sound(sound.SOUND_TYPE_KEY_ADDITION, 'type.wav')
engine.set_sound(sound.SOUND_TYPE_CLICK_MOUSE, 'type.wav')
menu.set_sound(engine, recursive=True)
pygame.mixer.music.load(path.join(snd_dir, 'HeroicDemise.mp3'))
pygame.mixer.music.set_volume(0.22)
pygame.mixer.music.play(loops=-1)

while True:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(surface)

    pygame.display.update()

pygame.quit()