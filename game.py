import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path

from coin import Coin
from enemy import Enemy
from exit import Exit
from lava import Lava
from player import Player
from world import World

# audio
pygame.mixer.pre_init(44100, -16, 2, 512) # TODO this configures sound, keep or remove
mixer.init()

pygame.init()
clock = pygame.time.Clock()
fps = 60

# initialise window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')
bg_img = pygame.image.load('media/sky.png')

# initialise sprites
#Provisional ( probably can be improved)
blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
player = Player(100,0)

game_over = 0
level = 0
# load in level data and create world
world = World(level,platform_group)

# main game loop
run = True
while (run): # this keeps the window up for now, replace with main game loop eventually
    clock.tick(fps) # cap the frame rate at 60 fps

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
    
    # drawing the display
    screen.blit(bg_img, (0,0))
    world.draw(screen)
    platform_group.draw(screen)
    
    
    game_over = player.update(game_over,screen,world, platform_group)

    pygame.display.update()

pygame.quit()