from pygame import *
import os

PLATFORM_WIDTH = 65
PLATFORM_HEIGHT = 70

wall = image.load('wall2.png')
wall = transform.scale(wall, (65,70))

class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = wall
        self.rect = self.image.get_rect()
        self.rect = (x, y)
