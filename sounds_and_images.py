from os import path
import pygame

snd_dir = path.join(path.dirname(__file__), 'sounds')
img_dir = path.join(path.dirname(__file__), 'image')

pygame.mixer.init()

missfire_sound = pygame.mixer.Sound(path.join(snd_dir, 'missfire.mp3'))
missfire_sound.set_volume(0.3)
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'shooti1.wav'))
shoot_sound.set_volume(0.08)



chest_sound = pygame.mixer.Sound(path.join(snd_dir, 'chest.mp3'))
chest_sound.set_volume(0.7)
elixir_sound = pygame.mixer.Sound(path.join(snd_dir, 'elixir.mp3'))
elixir_sound.set_volume(0.5)
eat_sound = pygame.mixer.Sound(path.join(snd_dir, 'potion2.mp3'))
eat_sound.set_volume(0.8)
gun_sound = pygame.mixer.Sound(path.join(snd_dir, 'gun.wav'))
gun_sound.set_volume(0.3)
tomato_sound = pygame.mixer.Sound(path.join(snd_dir, 'tomato.wav'))
tomato_sound.set_volume(0.3)
watermelon_sound = pygame.mixer.Sound(path.join(snd_dir, 'watermelon.wav'))
watermelon_sound.set_volume(0.25)
paper = pygame.mixer.Sound(path.join(snd_dir, 'intr.wav'))
paper.set_volume(0.15)

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
Gun2 = pygame.image.load(path.join(img_dir,'Gun.png'))
Gun2 = pygame.transform.scale(Gun2, (30,30))
Dyn = pygame.image.load(path.join(img_dir,'watermelon40.png'))
ghost = pygame.image.load(path.join(img_dir,'g.png'))
heart = pygame.image.load(path.join(img_dir,'heart.png'))
heart = pygame.transform.scale(heart, (30,30))
food_picture = pygame.image.load(path.join(img_dir,'Food.png'))
food_picture = pygame.transform.scale(food_picture, (30,30))