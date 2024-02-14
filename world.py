import pygame
from math import floor
from global_vars import *
from enemy import *

class World():
        def __init__(self,data,screen,enemies_group, globalVars):
            self.screen = screen
            self.globalVars = globalVars
            self.tile_list = []
            suelo = pygame.image.load('Assets/img/tile_1.png')
            
            row_count = 0
            for row in data:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        img = pygame.transform.scale(suelo, (TILE_SIZE, TILE_SIZE))
                        img_rect = img.get_rect()
                        img_rect.x = (col_count * TILE_SIZE)
                        img_rect.y = row_count * TILE_SIZE
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                    if tile == 2:
                        en = Enemy(col_count * TILE_SIZE, row_count * TILE_SIZE - 52, self.globalVars)                    
                        enemies_group.add(en)
                    col_count += 1
                row_count += 1

        def update(self):
            for tile in self.tile_list:
                tile[1].x -= self.globalVars.CAMERA_OFFSET_X
                self.screen.blit(tile[0], tile[1])

    