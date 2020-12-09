from os import path
import pygame

snd_dir = path.join(path.dirname(__file__), 'sounds')
img_dir = path.join(path.dirname(__file__), 'image')

pygame.mixer.init()

missfire_sound = pygame.mixer.Sound(path.join(snd_dir, 'missfire.mp3'))
missfire_sound.set_volume(0.3)
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'shooti1.wav'))
shoot_sound.set_volume(0.08)



chest_sound = pygame.mixer.Sound(path.join(snd_dir, 'coin1.wav'))
chest_sound.set_volume(0.05)
gun_sound = pygame.mixer.Sound(path.join(snd_dir, 'gun.wav'))
gun_sound.set_volume(0.3)
tomato_sound = pygame.mixer.Sound(path.join(snd_dir, 'tomato.wav'))
tomato_sound.set_volume(0.3)
watermelon_sound = pygame.mixer.Sound(path.join(snd_dir, 'watermelon.wav'))
watermelon_sound.set_volume(0.3)

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
dyn = pygame.image.load(path.join(img_dir,'watermelon40.png'))
ghost = pygame.image.load(path.join(img_dir,'g.png'))

