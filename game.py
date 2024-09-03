import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path
import Player, World, Enemy, Exit, Lava, Coin


pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

# window stuff

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

#Provisional ( probably can be improved)
blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# window background

bg_img = pygame.image.load('media/sky.png')

player = Player.Player(100,0)
game_over = 0

level = 0
# load in level data and create world
world = World.World(level,platform_group)
run = True
while (run): # this keeps the window up for now, replace with main game loop eventually
    clock.tick(fps)
    
    screen.blit(bg_img, (0,0))
    world.draw(screen)
    platform_group.draw(screen)
    
    
    game_over = player.update(game_over,screen,world, platform_group)

    pygame.display.update()
