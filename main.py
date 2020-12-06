import random
from Weapon import *
from Item import *
from pygame.math import Vector2
import pygame_menu
from pygame_menu import sound
import time
from Map import *
from sounds_and_images import *

#snd_dir = path.join(path.dirname(__file__), 'sounds')
#img_dir = path.join(path.dirname(__file__), 'image')

#картинки


pygame.init()





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

class Monster(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_stand
        self.rect = self.image.get_rect()
        self.rect.center = Vector2(pos)
        self.speed = Vector2(0,0)
        self.left, self.right, self.up, self.down = 0, 0, 0, 1
        self.vel = 4 #величина скорости
        self.health = 60

    def update(self):
        self.speed = Vector2(0,0)
        "Попадание пули в монстра"
        if (pygame.sprite.groupcollide(monsters, bullets, False, False)):
            if(player.Weap == Gun):
                self.health -= 10
                if (self.health <= 0):
                    pygame.sprite.groupcollide(monsters, bullets, True, True)
                else:
                    pygame.sprite.groupcollide(monsters, bullets, False, True)
            if (player.Weap == Tomato):
                self.health -= 5
                if (self.health <= 0):
                    pygame.sprite.groupcollide(monsters, bullets, True, True)
                else:
                    pygame.sprite.groupcollide(monsters, bullets, False, True)
            if (player.Weap == Dynamite):
                pygame.sprite.groupcollide(monsters, bullets, True, True)

        "Тут реализовано движение монстра"
        if((player.rect.x - self.rect.x) ** 2 + (player.rect.y - self.rect.y) ** 2 < (500)**2):
            if ((~checkMoveLeft(MAP, self.rect.topleft, self.rect.bottomleft) & (sign(player.rect.x - self.rect.x) == -1)) | (~checkMoveRight(MAP, self.rect.topright, self.rect.bottomright) & (sign(player.rect.x - self.rect.x) == 1))):
                self.speed.x = 0
                if (sign(player.rect.y - self.rect.y) == -1 & ~checkMoveUp(MAP, self.rect.topleft, self.rect.topright)):
                    self.speed.y = 0
                elif (sign(player.rect.y - self.rect.y) == 1 & ~checkMoveDown(MAP, self.rect.bottomleft, self.rect.bottomright)):
                    self.speed.y = 0
                else:
                    self.speed.y = self.vel * sign(player.rect.y - self.rect.y)
            elif ((~checkMoveUp(MAP, self.rect.topleft, self.rect.topright) & (sign(player.rect.y - self.rect.y) == -1)) | (~checkMoveDown(MAP, self.rect.bottomleft, self.rect.bottomright) & (sign(player.rect.y - self.rect.y) == 1))):
                self.speed.x = self.vel * sign(player.rect.x - self.rect.x)
                self.speed.y = 0
            else:
                if (player.rect.x - self.rect.x > player.rect.y - self.rect.y):
                    self.speed.x = self.vel * sign(player.rect.x - self.rect.x)
                    self.speed.y = self.vel * sign(player.rect.y - self.rect.y) // 2
                else:
                    self.speed.y = self.vel * sign(player.rect.y - self.rect.y)
                    self.speed.x = self.vel * sign(player.rect.x - self.rect.x) // 2

        else:
            self.speed.x = 0
            self.speed.y = 0

        self.rect.x += self.speed.x
        self.rect.y += self.speed.y

class Dynamite(Weapon):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = dyn
        self.rect = self.image.get_rect()
        self.vel = 2
        self.rect.center = pos

    def update(self):
        if self.direction == 'RIGHT':
            self.speed.x = self.vel
            self.speed.y = 0
        elif self.direction == 'LEFT':
            self.speed.x = -self.vel
            self.speed.y = 0
        elif self.direction == 'DOWN':
            self.speed.y = self.vel
            self.speed.x = 0
        elif self.direction == 'UP':
            self.speed.y = -self.vel
            self.speed.x = 0
        self.rect.center += self.speed
        # убить, если он заходит за верхнюю часть экрана
        pygame.sprite.groupcollide(platforms, bullets, True, False)
        if self.rect.y < 0 or self.rect.x < 0 or checkDynamite(MAP, self.rect.center, 1):
            self.kill()

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
        self.Weap = Tomato
        self.gun = 0 #кол-во патронов
        self.dyn = 0 #кол-во патронов
        self.health = 150

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

        "Уменьшается здоровье при столкновении с монстром"
        if (pygame.sprite.spritecollide(player, monsters,  False)):
            self.health -=  1
        print(self.health) #отладка

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

    def check_patron(self):
        shoot = 0
        if (self.Weap == Gun and self.gun > 0):
            self.shoot()
            self.gun -= 1
            shoot = 1
        elif (self.Weap == Dynamite and self.dyn > 0):
            self.shoot()
            self.dyn -= 1
            shoot = 1
            shoot_sound.play()

        elif self.Weap == Tomato:
            self.shoot()
            shoot = 1
        if shoot == 0:
            missfire_sound.play()


class Dynamite(Weapon):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = dyn
        self.rect = self.image.get_rect()
        self.vel = 2
        self.rect.center = pos

    def update(self):
        if self.direction == 'RIGHT':
            self.speed.x = self.vel
            self.speed.y = 0
        elif self.direction == 'LEFT':
            self.speed.x = -self.vel
            self.speed.y = 0
        elif self.direction == 'DOWN':
            self.speed.y = self.vel
            self.speed.x = 0
        elif self.direction == 'UP':
            self.speed.y = -self.vel
            self.speed.x = 0
        self.rect.center += self.speed
        # убить, если он заходит за верхнюю часть экрана
        pygame.sprite.groupcollide(platforms, bullets, True, False)
        if self.rect.y < 0 or self.rect.x < 0 or checkDynamite(MAP, self.rect.center, 1):
            self.kill()


# Создаем игру и окно




#добавление спрайтов
all_sprites = pygame.sprite.Group()
items = pygame.sprite.Group()
bullets = pygame.sprite.Group()
monsters = pygame.sprite.Group()#для отладки!!!
player = Player((total_level_width//2, total_level_height//2))
monster = Monster((total_level_width//2, total_level_height//2)) #для отладки!!!!
monsters.add(monster)#для отладки!!!


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
all_sprites.add(monster)

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
                        n = random.randint(0,5) #рандомное целое на отрезке. для вероятности.
                        if n != 4 and n != 5:
                            score += 1
                            chest_sound.play()
                        elif n == 4:
                            player.Weap = Gun
                            gun_sound.play()
                            player.gun += 5
                        elif n == 5:
                            player.Weap = Dynamite
                            watermelon_sound.play()
                            player.dyn += 2
                if event.key == pygame.K_SPACE:
                    player.check_patron()
                if event.key == pygame.K_r:
                    if player.Weap == Gun:
                        player.Weap = Dynamite
                        watermelon_sound.play()
                    elif player.Weap == Dynamite:
                        player.Weap = Tomato
                        tomato_sound.play()
                    elif player.Weap == Tomato:
                        player.Weap = Gun
                        gun_sound.play()



        # Обновление
        all_sprites.update()
        #if(player.Weap == Dynamite):
            #pygame.sprite.groupcollide(platforms, bullets, True, True)
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
            draw_text(screen, str(player.gun), 18, 70, 25)
        elif player.Weap == Dynamite:
            screen.blit(dyn, Vector2(10, 10))
            draw_text(screen, str(player.dyn), 18, 70, 25)
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