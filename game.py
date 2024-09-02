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

bg_img = pygame.image.load('media/sky.png')

player = Player.Player(100,0)
game_over = 0

level = 0
# load in level data and create world
World = World.World(level)
run = True
while (run): # this keeps the window up for now, replace with main game loop eventually
    clock.tick(fps)
    
    screen.blit(bg_img, (0,0))
    World.draw(screen)
    game_over = player.update(game_over,screen)
    pygame.display.update()
