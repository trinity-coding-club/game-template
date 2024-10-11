import pygame
from os import path
import csv

from world_platform import Platform
from Enemy import Enemy
from Lava import Lava
from Exit import Exit
from Coin import Coin

class World():
    """
    The game world, made up of tiles, platforms, lava, enemies, coins, and a single exit.

    Parameters:
        level: The number of the level file to read from to construct the world (e.g. 0 for level0.txt)
    """

    def __init__(self, level):
        """
        Create a world by reading level data from a file and converting it to sprites to be 
        drawn on the screen.
        """

        world_data = self.get_data_from_file(level)

        tile_size = 40
        self.tile_list = []

        # initialise sprite groups
        self.platform_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.lava_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()

        # load images
        dirt_img = pygame.image.load('media/dirt.png')
        grass_img = pygame.image.load('media/grass.png')

        # iterate through world_data and read each cell of the grid
        # TODO make this more readable
        row_count = 0
        for row in world_data:
            col_count = 0
            for tile in row:

                if tile == 1: # dirt
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 2: # grass
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 3: # enemy
                    enemy = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    self.enemy_group.add(enemy)

                if tile == 4: # platform
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0,tile_size)
                    self.platform_group.add(platform)

                if tile == 5: # platform
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1,tile_size)
                    self.platform_group.add(platform)

                if tile == 6: # lava
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2), tile_size)
                    self.lava_group.add(lava)

                if tile == 7: # coin
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2), tile_size)
                    self.coin_group.add(coin)

                if tile == 8: # exit door
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2), tile_size)
                    self.exit_group.add(exit)

                col_count += 1
            row_count += 1

    def draw(self, screen):
        """Draw the world on the screen."""
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
        self.enemy_group.draw(screen)
        self.coin_group.draw(screen)
        self.lava_group.draw(screen)
        self.exit_group.draw(screen)
        self.platform_group.draw(screen)

    def update(self):
        self.enemy_group.update()
        self.platform_group.update()

    def get_platform_group(self):
        return self.platform_group

    @staticmethod
    def get_data_from_file(level_num):
        """
        Read level data from a csv file into a list.

        Parameters:
            level_num: The number of the level file to read from, e.g. 0 for levels0.csv
        Returns:
            world_data: A 2D int array representing the tile grid that makes up the world.
            Each internal array represents a row of the tile grid.
        """

        if path.exists(f'levels/level{level_num}.csv'):
            world_data = []
            with open(f'levels/level{level_num}.csv', 'r') as level_file:
                for line in csv.reader(level_file):
                    world_data.append([int(x) for x in line])
        else:
            raise FileNotFoundError(f"levels/level{level_num}.csv")

        return world_data