import pygame
import json
from Entities.Enemies.enemy import *
from Entities.Player.pistol import *
from Interactives.computer import Computer
from Constants.constants import *

class World():
        def __init__(self, enemies, enemyFactory, interactives, cameraOffset):
            self.tile_list = []
            self.gun_list = []
            self.terrainHitBoxList = []
            self.platformsHitBoxList = []
            self.interactuableList = []

            self.enemyFactory = enemyFactory
            pistola = pygame.image.load(PLAYER_PATH + '/pistol.png')
            pistola2 = pygame.image.load(PLAYER_PATH + '/pistol2.png')
            pistola3 = pygame.image.load(PLAYER_PATH + '/pistol3.png')
            ordenador = pygame.image.load(INTERACTIVES_PATH + '/ibm5150.png')
        
            '''row_count = 0
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
                        img_rect = img.get_rect()
                        img_rect.x = (col_count * TILE_SIZE)
                        img_rect.y = row_count * TILE_SIZE
                        
                        hit_box = img.get_rect()
                        hit_box.x = (col_count
                          * TILE_SIZE)
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
                row_count += 1'''
            self.cargarNivel("Lvl1")

            '''print("Numero de tiles en el terreno antes: ")
            print(len(self.tile_list))
            print("Numero de tiles en el terreno ahora: ")
            print(len(self.terrainHitBoxList))


            print("Numero de tiles en el terreno antes: ")
            print(len(self.tile_list))
            print("Numero de tiles en el terreno ahora: ")
            print(len(self.terrainHitBoxList))'''

        def inicialOffset(self, cameraOffset):

            (cameraOffsetX,cameraOffsetY) = cameraOffset
            
            for tile in self.tile_list:
                tile[1].x -= cameraOffsetX
                tile[1].y -= cameraOffsetY

            for gun in self.gun_list:
                gun[1].x -= cameraOffsetX
                gun[1].y -= cameraOffsetY

            for hitbox in self.terrainHitBoxList:
                hitbox.x -= cameraOffsetX
                hitbox.y -= cameraOffsetY

            for hitbox in self.platformsHitBoxList:
                hitbox.x -= cameraOffsetX
                hitbox.y -= cameraOffsetY



        def draw(self, screen, cameraOffset):
            # Se dibuja las tiles teniendo en cuenta el scroll

            (cameraOffsetX,cameraOffsetY) = cameraOffset

            for tile in self.tile_list:
                tile[1].x -= cameraOffsetX
                tile[1].y -= cameraOffsetY
                screen.blit(tile[0], tile[1])

            for gun in self.gun_list:
                gun[1].x -= cameraOffsetX
                gun[1].y -= cameraOffsetY
                screen.blit(gun[0], gun[1])

            for hitbox in self.terrainHitBoxList:
                hitbox.x -= cameraOffsetX
                hitbox.y -= cameraOffsetY
            
            for hitbox in self.platformsHitBoxList:
                hitbox.x -= cameraOffsetX
                hitbox.y -= cameraOffsetY


        def seleccionarTextura(self, fila, columna, maxColumna, altura, anchura, imagen):
            if columna >= maxColumna:
                return self.seleccionarTextura(fila+1, columna-10, maxColumna, altura, anchura, imagen)
            else:
                return imagen.subsurface((columna*anchura, fila*altura, anchura, altura))
            
        def loadMap(self, map, compression, columns, tileHeight, tileWidth, textures, mapWidth):
            
             # Iniciar la posicion del mapa
            mapaX = 0
            mapaY = 0
            previousTileId = 0

            # Se recorre el nivel tile por tile
            for tile in map:
                # Si un tile
                if tile > 0:
                    # Se recupera la textura que representa el tile y se añade una hitbox
                    texture = self.seleccionarTextura(0, tile+compression, columns, tileHeight, tileWidth, textures)
                    textureRect = texture.get_rect()
                    textureRect.x = mapaX * tileWidth
                    textureRect.y = mapaY * tileHeight
                    tileTuple = (texture, textureRect)
                    self.tile_list.append(tileTuple)

                    if previousTileId == 1:
                        self.terrainHitBoxList.pop()
                        joinedHitBox = previousTile.union(textureRect)
                        previousTile = joinedHitBox
                        self.terrainHitBoxList.append(joinedHitBox)
                    else:
                        self.terrainHitBoxList.append(texture.get_rect())
                        previousTile = textureRect

                    previousTileId = 1
                
                else: 
                    previousTileId = 0
                    
                # Se actualiza la posicion del mapa
                mapaX += 1
                if mapaX >= mapWidth:
                    mapaX = 0
                    mapaY += 1

        def loadPlatforms(self, map, compression, columns, tileHeight, tileWidth, textures, mapWidth):
            
             # Iniciar la posicion del mapa
            mapaX = 0
            mapaY = 0
            previousTileId = 0

            # Se recorre el nivel tile por tile
            for tile in map:
                # Si un tile
                if tile > 0:
                    # Se recupera la textura que representa el tile y se añade una hitbox
                    texture = self.seleccionarTextura(0, tile+compression, columns, tileHeight, tileWidth, textures)
                    textureRect = texture.get_rect()
                    textureRect.x = mapaX * tileWidth
                    textureRect.y = mapaY * tileHeight
                    tileTuple = (texture, textureRect)
                    self.tile_list.append(tileTuple)

                    if previousTileId == 1:
                        self.platformsHitBoxList.pop()
                        joinedHitBox = previousTile.union(textureRect)
                        previousTile = joinedHitBox
                        self.platformsHitBoxList.append(joinedHitBox)
                    else:
                        self.platformsHitBoxList.append(texture.get_rect())
                        previousTile = textureRect

                    previousTileId = 1
                
                else: 
                    previousTileId = 0
                    
                # Se actualiza la posicion del mapa
                mapaX += 1
                if mapaX >= mapWidth:
                    mapaX = 0
                    mapaY += 1

        def getPlatforms(self):
            return self.platformsHitBoxList

        def loadBackground(self, background, compression, columns, tileHeight, tileWidth, textures, mapWidth):
            mapaX = 0
            mapaY = 0

            # Se recorre el nivel tile por tile
            for tile in background:
                # Si un tile
                if tile > 0:
                    # Se recupera la textura que representa el tile y se añade una hitbox
                    texture = self.seleccionarTextura(0, tile+compression, columns, tileHeight, tileWidth, textures)
                    textureRect = texture.get_rect()
                    textureRect.x = mapaX * tileWidth
                    textureRect.y = mapaY * tileHeight
                    tileTuple = (texture, textureRect)
                    self.tile_list.append(tileTuple) 
                    
                # Se actualiza la posicion del mapa
                mapaX += 1
                if mapaX >= mapWidth:
                    mapaX = 0
                    mapaY += 1
            
        def cargarNivel(self, nivel):

            # Cargar el json con los datos del nivel

            with open(LVLS_PATH + nivel + '/datosNivelB.json', 'r') as file:
                nivelData = file.read()
            nivelData = json.loads(nivelData)
            mapaNivel1 = nivelData['layers'][1]
            platforms = nivelData['layers'][2]['data']
            map = mapaNivel1['data']
            mapWidth = mapaNivel1['width']
            compression = nivelData['compressionlevel']

            # Cargar el json con los datos de las texturas

            pathTextura = nivelData['tilesets'][0]['source']
            with open(LVLS_PATH + nivel + "/" + pathTextura, 'r') as file:
                texturasNivel = file.read()
            texturasNivel = json.loads(texturasNivel)
            columns = texturasNivel['columns']
            tileHeight = texturasNivel['tileheight']
            tileWidth = texturasNivel['tilewidth']

            # Cargar la imagen con las texturas de los tiles
            textures = pygame.image.load(LVLS_PATH + nivel + '/texturas.png') 

            background = pygame.image.load(LVLS_PATH + nivel + '/background.png')

            backgroundRect = background.get_rect()
            self.tile_list.append((background, backgroundRect)) 
            self.loadMap(map, compression, columns, tileHeight, tileWidth, textures, mapWidth)
            self.loadPlatforms(platforms, compression, columns, tileHeight, tileWidth, textures, mapWidth)
            


            


           

        
            
