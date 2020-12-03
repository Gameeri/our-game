from pygame import *
from os import path

img_dir = path.join(path.dirname(__file__), 'image')

PLATFORM_WIDTH = 65
PLATFORM_HEIGHT = 70

wall = image.load(path.join(img_dir,'wall2.png'))
wall = transform.scale(wall, (65,70))

class Platform(sprite.Sprite):
    def __init__(self, pos):
        sprite.Sprite.__init__(self)
        self.image = wall
        self.rect = self.image.get_rect()
        #я добавил вот эту штучку
        self.rect.topleft = pos