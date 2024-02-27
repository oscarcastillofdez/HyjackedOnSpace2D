import pygame
from math import floor
from global_vars import *
from enemy import *
from pistol import *
from computer import Computer

class World():
        def __init__(self, globalVars, enemies, enemyFactory, interactuable):
            self.globalVars = globalVars
            self.tile_list = []
            self.gun_list = []
            self.terrainHitBoxList = []
            self.interactuableList = []

            self.enemyFactory = enemyFactory

            suelo = pygame.image.load('Assets/img/tile_1.png')
            pistola = pygame.image.load('Assets/img/pistol.png')
            pistola2 = pygame.image.load('Assets/img/pistol2.png')
            pistola3 = pygame.image.load('Assets/img/pistol3.png')
            ordenador = pygame.image.load('Assets/img/ibm5150.png')
            
            # Se dibuja las tiles en el mundo
            img = pygame.transform.scale(suelo, (TILE_SIZE, TILE_SIZE))
            img_rect = img.get_rect()

            previousTile = (img, img_rect)
            previousTileId = 0

            row_count = 0
            for row in globalVars.world_data:
                col_count = 0
                previousTileId = -1
                
                for tile in row: 
                    
                    # Podria hacerse cuatro listas (O las que se quisieran)
                    # 1º Contedria todos los tiles de la mitad superior izquierda del nivel
                    # 2º Contendria todos los tiles de la mitad superior derecha del nivel
                    # 3º Contendria todos los tiles de la mitad inferior izquierda del nivel
                    # 4º Contendria todos los tiles de la mitad inferior derecha del nivel
                    # Los sprites no se meterian en estas listas, tendrian una sola lista (NO va  a haber 1000 sprites, pero si tiles)
                    # Se comprobaria en que región (en cual de las cuatro listas) esta el personaje y se comrpobarian las colisiones con los tiles presentes en esa region
                    # Es decir se recorrerian las 4 regiones buscando si el personaje está en cada una de ellas (com collidelist se podria conrpobar si el jugador esta dentro de esta region)
                    # O el personaje podria informar (patron observer) en que region esta
                    # Pero esperar a que oscar lo haga con JSON primero

                    # Tambien se podria simultaneamente los tiles que estan juntos juntarlos mediante union() para hacer solo un rectangulo
                    if tile == 0:
                        previousTileId = 0
                    if tile == 1:
                        img = pygame.transform.scale(suelo, (TILE_SIZE, TILE_SIZE))
                        img_rect = img.get_rect()
                        img_rect.x = (col_count * TILE_SIZE)
                        img_rect.y = row_count * TILE_SIZE
                        
                        hit_box = img.get_rect()
                        hit_box.x = (col_count * TILE_SIZE)
                        hit_box.y = row_count * TILE_SIZE

                        tile = (img, img_rect)

                        if previousTileId == 1:
                            self.terrainHitBoxList.pop()
                            joinedHitBox = previousTile.union(hit_box)
                            previousTile = joinedHitBox
                            self.terrainHitBoxList.append(joinedHitBox)
                        else:
                            self.terrainHitBoxList.append(hit_box)
                            previousTile = hit_box

                        self.tile_list.append(tile)
                        
                        previousTileId = 1

                    if tile == 2:
                        en = self.enemyFactory.createEnemy(col_count * TILE_SIZE, row_count * TILE_SIZE - 52, self.globalVars)
                        enemies.add(en)
                        previousTileId = 2

                    if tile == 3:
                        img = pygame.transform.scale(pistola, (TILE_SIZE, TILE_SIZE))
                        img_rect = img.get_rect()
                        img_rect.x = (col_count * TILE_SIZE)
                        img_rect.y = row_count * TILE_SIZE
                        tile = (img, img_rect)
                        self.gun_list.append(tile)
                        previousTileId = 3
                    if tile == 4:
                        ordenador = Computer(col_count * TILE_SIZE, row_count * TILE_SIZE, self.globalVars)
                        interactuable.add(ordenador)
                        previousTileId = 4
                    col_count += 1
                row_count += 1


            print("Numero de tiles en el terreno antes: ")
            print(len(self.tile_list))
            print("Numero de tiles en el terreno ahora: ")
            print(len(self.terrainHitBoxList))

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

            for hitbox in self.terrainHitBoxList:
                hitbox.x -= globalVars.CAMERA_OFFSET_X
                hitbox.y -= globalVars.CAMERA_OFFSET_Y