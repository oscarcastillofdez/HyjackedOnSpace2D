import pygame
import json
from Entities.Enemies.enemy import *
from Entities.Player.playerWithPistol import *
from Entities.shieldPickup import ShieldPickup
from Interactives.computer import Computer
from Constants.constants import *
from Entities.health import Health
from Entities.grenadeLauncher import GrenadeLauncher
from Entities.pistol import Pistol

class World():
        def __init__(self, enemies, enemyFactory, interactives, cameraOffset, healthPickUps, destructibles_group, gunPickups):
            self.tile_list = []
            self.gun_list = []
            self.terrainHitBoxList = []
            self.platformsHitBoxList = []
            self.interactuableList = []
            self.enemies = enemies
            self.healthPickUps = healthPickUps
            self.destructibles_group = destructibles_group
            self.gunPickups = gunPickups
            self.interactiveGroup = interactives

            self.enemyFactory = enemyFactory
            self.pistola = pygame.transform.scale(pygame.image.load(PLAYER_PATH + '/pistol.png'), (45,45))
            pistola2 = pygame.image.load(PLAYER_PATH + '/pistol2.png')
            pistola3 = pygame.image.load(PLAYER_PATH + '/pistol3.png')
            ordenador = pygame.image.load(INTERACTIVES_PATH + '/ibm5150.png')

            self.shieldImage = pygame.transform.scale(pygame.image.load(PLAYER_PATH + '/plasma_shield.png'), (45,45))
            self.cargarNivel("Lvl1")


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
                gun[0][1].x -= cameraOffsetX
                gun[0][1].y -= cameraOffsetY
                screen.blit(gun[0][0], gun[0][1])

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

        def loadEntities(map):

            mapaX = 0
            mapaY = 0
            
            for tile in map:
                

                # TODO: Hacer pistola y shield un objeto propio, 
                # facilitara el saber si se recogio una cosa u otra 
                # y se le quitaria trabajo a la clase update() del player (actualmente comprueba colision con todos los pickups)
                if mapaX == 14 and mapaY == 31:
                    pistol = Pistol(mapaX * tileWidth, mapaY * tileHeight)
                    self.gunPickups.add(pistol)
                
                if mapaX == 20 and mapaY == 31:
                    shieldPickup = ShieldPickup(mapaX * tileWidth, mapaY * tileHeight)
                    self.gunPickups.add(shieldPickup)

                if mapaX == 26 and mapaY == 31:
                    grenadeLauncher = GrenadeLauncher(mapaX * tileWidth, mapaY * tileHeight)
                    self.gunPickups.add(grenadeLauncher)

                if mapaX == 50 and mapaY == 31:
                    health = Health(mapaX * tileWidth, mapaY * tileHeight)
                    self.healthPickUps.add(health)

                if mapaX == 30 and mapaY == 31:
                    en = self.enemyFactory.createEnemy(mapaX * tileWidth, mapaY * tileHeight)
                    self.enemies.add(en)
                    print("A")

                if mapaX == 30 and mapaY == 31:
                    computer = Computer(mapaX * tileWidth, mapaY * tileHeight)
                    self.interactiveGroup.add(computer)
                    print("A")

                if mapaX == 30 and mapaY == 31:
                    textureRect = pygame.Rect(mapaX * tileWidth, mapaY * tileHeight, tileWidth,tileHeight)
                    self.terrainHitBoxList.append(textureRect)

                    en = self.enemyFactory.createEnemy2(mapaX * tileWidth, mapaY * tileHeight, textureRect)
                    self.destructibles_group.add(en)

                

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
            


            


           

        
            
