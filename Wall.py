from pygame import *
from pygame.math import Vector2
import os

PLATFORM_WIDTH = 65
PLATFORM_HEIGHT = 70

wall = image.load('wall2.png')
wall = transform.scale(wall, (65,70))

class Platform(sprite.Sprite):
    def __init__(self, pos):
        sprite.Sprite.__init__(self)
        self.image = wall
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
