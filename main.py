import random
from Weapon import *
from Item import *
from pygame.math import Vector2
import pygame_menu
from pygame_menu import sound
import time
from Map import *
from sounds_and_images import *

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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ghost
        self.rect = self.image.get_rect()
        "Начальные координаты монстра"
        pos = (0, 0)
        while (MAP.ourMap[pos[1]//WALL_HEIGHT][pos[0]//WALL_WIDTH] != 'e'):
            pos = (random.randint(2 * WALL_WIDTH, total_level_width-WALL_WIDTH), random.randint(2 * WALL_HEIGHT, total_level_height-WALL_HEIGHT))
        self.rect.center = Vector2(pos)

        self.speed = Vector2(0,0)
        self.left, self.right, self.up, self.down = 0, 0, 0, 1
        self.vel = 4 #величина скорости
        self.health = 50

    def update(self):
        self.speed = Vector2(0, 0)
        "Попадание пули в монстра"
        if (pygame.sprite.spritecollide(self, bullets, False)):
            if(player.Weap == Gun):
                self.health -= 10
                if (self.health <= 0):
                    pygame.sprite.groupcollide(monsters, bullets, True, True)
                else:
                    pygame.sprite.groupcollide(monsters, bullets, False, True)
            if (player.Weap == Tomato):
                self.health -= 3
                if (self.health <= 0):
                    pygame.sprite.groupcollide(monsters, bullets, True, True)
                else:
                    pygame.sprite.groupcollide(monsters, bullets, False, True)
            if (player.Weap == Dynamite):
                pygame.sprite.groupcollide(monsters, dynamites, True, True)
        pygame.sprite.groupcollide(monsters, dynamites, True, True)

        "Тут реализовано движение монстра"
        if((player.rect.x - self.rect.x) ** 2 + (player.rect.y - self.rect.y) ** 2 < (500)**2):
            if ((~checkMoveLeft(MAP, self.rect.topleft, self.rect.bottomleft) & (sign(player.rect.x - self.rect.x) == -1)) | (~checkMoveRight(MAP, self.rect.topright, self.rect.bottomright) & (sign(player.rect.x - self.rect.x) == 1))):
                self.speed.x = 0
                if (sign(player.rect.y - self.rect.y) == -1 & ~checkMoveUp(MAP, self.rect.topleft, self.rect.topright)):
                    self.speed.y = 0
                elif (sign(player.rect.y - self.rect.y) == 1 & ~checkMoveDown(MAP, self.rect.bottomleft, self.rect.bottomright)):
                    self.speed.y = 0
                else:
                    self.speed.y = self.vel * sign(player.rect.y - self.rect.y + 5)
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

class Dynamite(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = Dyn
        self.rect = self.image.get_rect()
        self.vel = 3
        self.rect.center = pos
        self.speed = Vector2(0, 0)
        self.direction = 'DOWN'

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
        pygame.sprite.groupcollide(platforms, dynamites, True, False)
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
        self.Weap = Tomato
        self.gun = 0 #кол-во патронов
        self.dyn = 0 #кол-во патронов
        self.health = 150
        self.food = 0

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



    def eat(self):
        if self.food > 0:
            self.food -= 1
            self.health += 5
            eat_sound.play()

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
            if self.Weap == Dynamite:
                all_sprites.add(bullet)
                dynamites.add(bullet)
                shoot_sound.play()
            else:
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

#добавление спрайтов
all_sprites = pygame.sprite.Group()
items = pygame.sprite.Group()
bullets = pygame.sprite.Group()
dynamites = pygame.sprite.Group()
monsters = pygame.sprite.Group()#для отладки!!!
player = Player((total_level_width//2, total_level_height//2))



for _ in range(10):  #добавление монстров
    monster = Monster()
    monsters.add(monster)
    all_sprites.add(monster)

platforms = pygame.sprite.Group()
platformsBorders = pygame.sprite.Group()
# счетчик


#отображение стен
coord = Vector2(0,0) # координаты
i = 0
for indexRow, row in enumerate(MAP.ourMap): # вся строка
    #это для определения координат пули
    j = 0
    for indexCol, col in enumerate(row): # каждый символ
        if col == "b":
            pf = Platform(coord)
            all_sprites.add(pf)
            if (indexRow == 0) | (indexRow == MAP_HEIGHT - 1) | (indexCol == 0) | (indexCol == MAP_WIDTH - 1):
                platformsBorders.add(pf)
            else:
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
def draw_text(surf, text, x, y, colour, font):
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Цикл игры

#предыстория
running = True
screen = pygame.display.set_mode((WIDTH, HEIGHT))
t = 0
background = pygame.image.load(path.join(img_dir, '80.jpg')).convert()
background_rect = background.get_rect()
pygame.display.set_caption("My Game")
pygame.mixer.music.load(path.join(snd_dir, 'Mysterious.mp3'))
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(loops=-1)
while(running):
    string1 = ""
    string2 = ""
    string3 = ""


    screen.blit(background, background_rect)

    if t == 0:
        string1 =  "Long time ago"
        string2 = "lived one elder"
    if t == 1:
        string1 = "He took care of "
        string2 = "his garden for centuries"
        string3 = " and cherished it"

    if t == 2:
        string1 = "One day evil spirits"
        string2 = "came from the"
        string3 = "neighboring lands"

    if t == 3:
        string1 = "They craved only"
        string2 = "destruction and blood"
        string3 = ""

    if t == 4:
        string2 = "The hope was dwindling..."
        string1 = ""
        string3 = ""


    draw_text(screen, string1,  WIDTH / 2, 170, BLACK, pygame.font.Font("fonts/Amano.ttf", 35))
    draw_text(screen, string2,  WIDTH / 2, 230, BLACK, pygame.font.Font("fonts/Amano.ttf", 35))
    draw_text(screen, string3,  WIDTH / 2, 290, BLACK, pygame.font.Font("fonts/Amano.ttf", 35))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            t+= 1
            paper.play()

    if t == 5:
        break
    pygame.display.flip()



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
                        if n == 1 or n == 0:
                            player.food += 1
                            elixir_sound.play()
                        elif n == 4:
                            player.Weap = Gun
                            gun_sound.play()
                            player.gun += 5
                        elif n == 5:
                            player.Weap = Dynamite
                            watermelon_sound.play()
                            player.dyn += 2
                        else:
                            chest_sound.play()
                if event.key == pygame.K_ESCAPE:
                    continue_menu()
                if event.key == pygame.K_SPACE:
                    player.check_patron()
                if event.key == pygame.K_q:
                    player.eat()
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


        if player.health <= 0:
            pygame.mixer.music.load(path.join(snd_dir, 'game_over.mp3'))
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(loops=-1)
            game_over()
        # Обновление
        all_sprites.update()

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

        if player.Weap == Tomato:
            screen.blit(tomato2, Vector2(20, 20))

        elif player.Weap == Gun:
            screen.blit(Gun2, Vector2(20, 20))
            draw_text(screen, str(player.gun), 70, 25, BLACK, pygame.font.Font("fonts/DS Stamper.ttf", 20))
        elif player.Weap == Dynamite:
            screen.blit(Dyn, Vector2(10, 10))
            draw_text(screen, str(player.dyn), 70, 25, BLACK, pygame.font.Font("fonts/DS Stamper.ttf", 20))

        screen.blit(heart, Vector2(590, 20))
        draw_text(screen, str(player.health), 575, 25, BLACK, pygame.font.Font("fonts/DS Stamper.ttf", 20))

        screen.blit(food_picture, Vector2(590, 55))
        draw_text(screen, str(player.food), 575, 60, BLACK, pygame.font.Font("fonts/DS Stamper.ttf", 20))

        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()

def game_over(): # меню завершения игры
    surface = pygame.display.set_mode((650, 500))
    pygame.display.set_caption("My Game")
    bkgr = pygame.image.load(path.join('image/main.jpg')).convert()
    neg = pygame.Surface(bkgr.get_size())
    neg.fill((255, 255, 255))
    neg.blit(bkgr, (0, 0), special_flags=pygame.BLEND_SUB)
    surface.blit(neg, neg.get_rect())



    while True:
        draw_text(surface, "Press any key to exit", WIDTH / 2, 400, WHITE, pygame.font.Font("fonts/AirmoleAntique Regular.ttf", 40))
        draw_text(surface, "GAME OVER", WIDTH / 2, 150, RED, pygame.font.Font("fonts/AirmoleAntique Regular.ttf", 100))
        events = pygame.event.get()



        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                exit()
        neg.blit(bkgr, (0, 0), special_flags=pygame.BLEND_SUB)
        #surface.blit(neg, (0,0))
        pygame.display.flip()


def continue_menu(): # меню паузы
    pygame.display.set_caption("My Game")
    surface = pygame.display.set_mode((650, 500))
    bkgr = pygame.image.load(path.join('image/main.jpg')).convert()
    menu = pygame_menu.Menu(250, 400, 'Pause',
                            theme=pygame_menu.themes.THEME_SOLARIZED )
    surface.blit(bkgr, bkgr.get_rect())
    menu.add_button('Continue', start_the_game)
    menu.add_button('Quit', pygame_menu.events.EXIT)

    engine = sound.Sound()
    engine.set_sound(sound.SOUND_TYPE_KEY_ADDITION, 'sounds/type43.wav')
    engine.set_sound(sound.SOUND_TYPE_CLICK_MOUSE, 'sounds/type43.wav')
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


#основное меню
surface = pygame.display.set_mode((650, 500))
bkgr = pygame.image.load(path.join('image/main.jpg')).convert()
menu = pygame_menu.Menu(300, 400, 'Main menu',
                       theme=pygame_menu.themes.THEME_SOLARIZED)
pygame.display.set_caption("My Game")
surface.blit(bkgr, bkgr.get_rect())
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

engine = sound.Sound()
engine.set_sound(sound.SOUND_TYPE_KEY_ADDITION, 'sounds/type43.wav')
engine.set_sound(sound.SOUND_TYPE_CLICK_MOUSE, 'sounds/type43.wav')
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