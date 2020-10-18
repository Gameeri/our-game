import pygame

player_stand = pygame.image.load('ded3.png')
player_right = pygame.image.load('ded_right2.png')
player_left = pygame.image.load('ded_left2.png')
player_up = pygame.image.load('ded_up2.png')
player_stand = pygame.transform.scale(player_stand, (60,55))
player_right = pygame.transform.scale(player_right, (60,55))
player_left = pygame.transform.scale(player_left, (60,55))
player_up = pygame.transform.scale(player_up, (60,55))

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_stand
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedx = 0
        self.speedy = 0
        self.left, self.right, self.up, self.down = 0, 0, 0, 0


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