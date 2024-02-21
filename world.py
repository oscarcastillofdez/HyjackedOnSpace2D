import pygame
from math import floor
from global_vars import *
from enemy import *
from pistol import *

class World():
        def __init__(self, globalVars, enemies):
            self.globalVars = globalVars
            self.tile_list = []
            self.gun_list = []

            suelo = pygame.image.load('Assets/img/tile_1.png')
            pistola = pygame.image.load('Assets/img/pistol.png')
            pistola2 = pygame.image.load('Assets/img/pistol2.png')
            pistola3 = pygame.image.load('Assets/img/pistol3.png')

            
            # Se dibuja las tiles en el mundo
            row_count = 0
            for row in globalVars.world_data:
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
                        enemies.add(en)
                    if tile == 3:
                        img = pygame.transform.scale(pistola, (TILE_SIZE, TILE_SIZE))
                        img_rect = img.get_rect()
                        img_rect.x = (col_count * TILE_SIZE)
                        img_rect.y = row_count * TILE_SIZE
                        tile = (img, img_rect)
                        self.gun_list.append(tile)

                    col_count += 1
                row_count += 1

        def draw(self, screen, globalVars):
            # Se dibuja las tiles teniendo en cuenta el scroll

            for tile in self.tile_list:
                tile[1].x -= globalVars.CAMERA_OFFSET_X
                tile[1].y -= globalVars.CAMERA_OFFSET_Y
                screen.blit(tile[0], tile[1])

            for gun in self.gun_list:
                gun[1].x -= globalVars.CAMERA_OFFSET_X
                gun[1].y -= globalVars.CAMERA_OFFSET_Y
                screen.blit(gun[0], gun[1])
    