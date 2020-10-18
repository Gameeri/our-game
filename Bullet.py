import pygame

RED = (255, 0, 0)
WIDTH = 650
HEIGHT = 700

tomato = pygame.image.load('tomato.png')
tomato = pygame.transform.scale(tomato, (20,20))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = tomato
        self.rect = self.image.get_rect()
        self.rect.bottom = y + 40
        self.rect.centerx = x
        self.speedy = self.speedx = 0
        self.direction = 'DOWN'

    def update(self):
        if self.direction == 'RIGHT':
            self.speedx = 10
            self.speedy = 0
        elif self.direction == 'LEFT':
            self.speedx = -10
            self.speedy = 0
        elif self.direction == 'DOWN':
            self.speedy = 10
            self.speedx = 0
        elif self.direction == 'UP':
            self.speedy = -10
            self.speedx = 0
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0 or self.rect.bottom > HEIGHT or self.rect.centerx < 0 or self.rect.centerx > WIDTH:
            self.kill()