import pygame
from os import path
import csv

from world_platform import Platform

class World():
    """
    The game world, made up of tiles.
    
    Parameters:
        level: The number of the level file to read from to construct the world (e.g. 0 for level0.txt)
        platform_group: the platform_group to add the world tiles to
    """

    def __init__(self, level, platform_group):
        """
        Create a world by reading level data from a file and converting it to a list 
        of tiles to be drawn on the screen.
        """

        # Initializig world variables
        self.tile_list = []
        data = self.get_data_from_file(level)
        tile_size = 40

        # load images
        dirt_img = pygame.image.load('media/dirt.png')
        grass_img = pygame.image.load('media/grass.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(
                        dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(
                        grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                # if tile == 3:
                #     blob = Enemy(col_count * tile_size,
                #                  row_count * tile_size + 15)
                #     blob_group.add(blob)
                if tile == 4:
                    platform = Platform(
                        col_count * tile_size, row_count * tile_size, 1, 0,tile_size)
                    platform_group.add(platform)
                if tile == 5:
                    platform = Platform(
                        col_count * tile_size, row_count * tile_size, 0, 1,tile_size)
                    platform_group.add(platform)
                # if tile == 6:
                #     lava = Lava(col_count * tile_size, row_count *
                #                 tile_size + (tile_size // 2))
                #     lava_group.add(lava)
                # if tile == 7:
                #     coin = Coin(col_count * tile_size + (tile_size // 2),
                #                 row_count * tile_size + (tile_size // 2))
                #     coin_group.add(coin)
                # if tile == 8:
                #     exit = Exit(col_count * tile_size, row_count *
                #                 tile_size - (tile_size // 2))
                #     exit_group.add(exit)
                col_count += 1
            row_count += 1

    def draw(self, screen):
        """Draw the world on the screen."""
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

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