import pygame
import pickle
from os import path
from world_platform import Platform

class World():
    def __init__(self, level,platform_group):
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
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

    @staticmethod  
    def get_data_from_file(level):
        if path.exists(f'levels/level{level}.txt'):
            pickle_in = open(f'levels/level{level}.txt', 'r')
            world_data = []
            for l in pickle_in:
                temp = []
                s_temp = l.strip().split(',')
            
                temp = [int(s) for s in s_temp]
            
                world_data.append(temp)
            
        return world_data
