import pygame
import yaml
import json
from math import floor
from global_vars import *
from Enemies.enemy import *
from Player.pistol import *
from Interactuables.computer import Computer
from constants import *

class World():
        def __init__(self, globalVars, enemies, enemyFactory, interactuable):
        
        def __init__(self, globalVars, enemies):
            self.globalVars = globalVars
            self.tile_list = []
            self.gun_list = []
            self.terrainHitBoxList = []
            self.interactuableList = []

            self.enemyFactory = enemyFactory

            tile0 = pygame.image.load('Assets/world/lvl1/TexturasSueltas/sueloSuperiorIzquierdo.png')
            tile1 = pygame.image.load('Assets/world/lvl1/TexturasSueltas/sueloSuperiorDerecho.png')
            tile2 = pygame.image.load('Assets/world/lvl1/TexturasSueltas/sueloSuperior.png')
            tile3 = pygame.image.load('Assets/world/lvl1/TexturasSueltas/sueloInferiorIzquierdo.png')
            tile4 = pygame.image.load('Assets/world/lvl1/TexturasSueltas/sueloInferiorDerecho.png')
            tile5 = pygame.image.load('Assets/world/lvl1/TexturasSueltas/sueloInferior.png')
            tile6 = pygame.image.load('Assets/world/lvl1/TexturasSueltas/paredCableIzquierda.png')
            tile7 = pygame.image.load('Assets/world/lvl1/TexturasSueltas/paredCableDerecha.png')
            tile8 = pygame.image.load('Assets/world/lvl1/TexturasSueltas/interseccionSuperiorIzquierda.png')
            tile9 = pygame.image.load('Assets/world/lvl1/TexturasSueltas/interseccionSuperiorDerecha.png')
            tile10 = pygame.image.load('Assets/world/lvl1/TexturasSueltas/interseccionInferiorIzquierda.png')
            tile11 = pygame.image.load('Assets/world/lvl1/TexturasSueltas/interseccionInferiorDerecha.png')
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
                    if tile >= 0 and tile < 20:
                        if tile == 0:
                            img = pygame.transform.scale(tile0, (TILE_SIZE, TILE_SIZE))
                        if tile == 1:
                            img = pygame.transform.scale(tile1, (TILE_SIZE, TILE_SIZE))
                        if tile == 2:
                            img = pygame.transform.scale(tile2, (TILE_SIZE, TILE_SIZE))
                        if tile == 3:
                            img = pygame.transform.scale(tile3, (TILE_SIZE, TILE_SIZE))
                        if tile == 4:
                            img = pygame.transform.scale(tile4, (TILE_SIZE, TILE_SIZE))
                        if tile == 5:
                            img = pygame.transform.scale(tile5, (TILE_SIZE, TILE_SIZE))
                        if tile == 6:
                            img = pygame.transform.scale(tile6, (TILE_SIZE, TILE_SIZE))
                        if tile == 7:
                            img = pygame.transform.scale(tile7, (TILE_SIZE, TILE_SIZE))
                        if tile == 8:
                            img = pygame.transform.scale(tile8, (TILE_SIZE, TILE_SIZE))
                        if tile == 9:
                            img = pygame.transform.scale(tile9, (TILE_SIZE, TILE_SIZE))
                        if tile == 10:
                            img = pygame.transform.scale(tile10, (TILE_SIZE, TILE_SIZE))
                        if tile == 11:
                            img = pygame.transform.scale(tile11, (TILE_SIZE, TILE_SIZE))
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

                    if tile == 50:
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
                self.cargarNivel("lvl1")

            
            


            print("Numero de tiles en el terreno antes: ")
            print(len(self.tile_list))
            print("Numero de tiles en el terreno ahora: ")
            print(len(self.terrainHitBoxList))


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
        def seleccionarTextura(self, fila, columna, maxColumna, altura, anchura, imagen):
            if columna >= maxColumna:
                return self.seleccionarTextura(fila+1, columna-9, maxColumna, altura, anchura, imagen)
            else: 
                rectangulo = (columna*anchura, fila*altura, anchura, altura)
                imagen = imagen.subsurface(rectangulo)
                return imagen
            
        def cargarNivel(self, nivel):
            with open(LVLS_PATH + nivel + '/datosNivel.json', 'r') as file:
                nivelData = file.read()

            nivelData = json.loads(nivelData)
            pathTextura = nivelData['tilesets'][0]['source']
            imagen = pygame.image.load(LVLS_PATH + nivel + '/texturas.png') 

            mapaNivel1 = nivelData['layers'][0]
            nivel1Grid = mapaNivel1['data']
            anchuraMapa = mapaNivel1['width']
            compresion = nivelData['compressionlevel']

            with open(LVLS_PATH + "lvl1/" + pathTextura, 'r') as file:
                texturasNivel = file.read()
            texturasNivel = json.loads(texturasNivel)

            columnas = texturasNivel['columns']
            tileHeight = texturasNivel['tileheight']
            tileWidth = texturasNivel['tilewidth']

            mapaX = 0
            mapaY = 0

            for tile in nivel1Grid:
                if tile > 0:
                    textura = self.seleccionarTextura(0, tile+compresion, columnas, tileHeight, tileWidth, imagen)
                    img_rect = textura.get_rect()
                    img_rect.x = mapaX * tileWidth
                    img_rect.y = mapaY * tileHeight
                    tile = (textura, img_rect)
                    self.tile_list.append(tile) 
                mapaX += 1
                if mapaX > anchuraMapa:
                    mapaX = 0
                    mapaY += 1
