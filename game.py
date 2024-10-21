import pygame
from pygame.locals import *
from pygame import mixer

from Player import Player
from World import World

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

# Initialise fonts for score and health display
font = pygame.font.SysFont('Bauhaus 93', 30)

# Function to draw text on the screen
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# initialise player
player = Player(50,500)

# initialise world
max_levels = 4
level_num = 4
world = World(level_num)

game_over = False

# main game loop
run = True
while (run): # this keeps the window up for now, replace with main game loop eventually
    clock.tick(fps) # cap the frame rate at 60 fps

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
    
    # draw the background, world and player onto the screen
    screen.blit(bg_img, (0,0))
    world.draw(screen)
    player.draw(screen)
    
    # update the player and the world
    game_over = player.update(game_over, screen, world)
    world.update()

    # Handle level completion or game over
    if game_over == 'level_completed':
        level_num += 1
        if level_num > max_levels:
            draw_text('Game Completed!', font, (255, 255, 0), screen_width // 2 - 100, screen_height // 2)
            pygame.display.update()
            pygame.time.delay(3000)
            run = False  # End the game after completion
        else:
            # Load next level
            world = World(level_num)
            player.rect.x = 50  # Reset player position
            player.rect.y = 500
            game_over = False  # Reset game_over for the new level

    # Display player's score and health
    draw_text(f'Score: {player.score}', font, (255, 255, 255), 10, 10)
    draw_text(f'Health: {player.health}', font, (255, 255, 255), 10, 50)

    # Check for Game Over
    if game_over:
        draw_text('Game Over', font, (255, 0, 0), screen_width // 2 - 100, screen_height // 2)
        pygame.display.update()
        pygame.time.delay(3000)  # Pause for 3 seconds
        run = False  # End the game

    # finally, update the screen with everything that has been drawn
    pygame.display.update()

pygame.quit()