import pygame
from os import path

img_dir = path.join(path.dirname(__file__), 'image')

item_picture = pygame.image.load(path.join(img_dir,'ChestRed.png'))
item_picture = pygame.transform.scale(item_picture, (33,33))

class Item(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = item_picture
        self.rect = self.image.get_rect()
        self.rect.topleft = pos