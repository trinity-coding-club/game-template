import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path
import Player, Enemy, Exit, Lava, Coin, World


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

# window background

bg_img = pygame.image.load('img/sky.png')

player = Player()

run = True
while (run): # this keeps the window up for now, replace with main game loop eventually
    clock.tick(fps)
    
    screen.blit(bg_img, (0,0))

    game_over = player.update(game_over)
    pygame.display.update()
