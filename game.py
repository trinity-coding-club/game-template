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

# initialise player
player = Player(100,0)

# initialise world
level_num = 0
world = World(level_num)

game_over = 0

# main game loop
run = True
while (run): # this keeps the window up for now, replace with main game loop eventually
    clock.tick(fps) # cap the frame rate at 60 fps

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
    
    # draw the background and world onto the screen
    screen.blit(bg_img, (0,0))
    world.draw(screen)
    
    game_over = player.update(game_over, screen, world)

    # finally, update the screen with everything that has been drawn
    pygame.display.update()

pygame.quit()