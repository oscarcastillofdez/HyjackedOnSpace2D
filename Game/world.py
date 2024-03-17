import pygame
import json
from Entities.Enemies.meleeEnemy import *
from Entities.Enemies.wallDestructible import WallDestructible
from Entities.Player.playerWithPistol import *
from Entities.pistolUpgrade import PistolUpgrade
from Entities.shieldPickup import ShieldPickup
from Interactives.computer import Computer
from Constants.constants import *
from Entities.health import Health
from Entities.grenadeLauncher import GrenadeLauncher
from Entities.pistol import Pistol
from Entities.dash import Dash
import Interactives.trigger as Trigger


class World():
        def __init__(self, lvl, enemies, enemyFactory, enemyFactorySecuence, interactives, cameraOffset, healthPickUps, destructibles_group, gunPickups,triggerGroup, dificulty, boss):
            self.tile_list = []
            self.platform_list = []
            self.background_list = []
            self.destructibleTile_list = []
            self.gun_list = []
            self.enemies = enemies
            self.dificulty = dificulty
            self.healthPickUps = healthPickUps
            self.destructibles_group = destructibles_group
            self.gunPickups = gunPickups
            self.interactiveGroup = interactives
            self.enemyFactory = enemyFactory
            self.triggerGroup = triggerGroup
            self.enemyFactorySecuence = enemyFactorySecuence
            self.boss = boss

            self.pistola = pygame.transform.scale(pygame.image.load(PLAYER_PATH + '/pistol.png'), (45,45))
            pistola2 = pygame.image.load(PLAYER_PATH + '/pistol2.png')
            pistola3 = pygame.image.load(PLAYER_PATH + '/pistol3.png')
            ordenador = pygame.image.load(INTERACTIVES_PATH + '/ibm5150.png')

            self.shieldImage = pygame.transform.scale(pygame.image.load(PLAYER_PATH + '/plasma_shield.png'), (45,45))
            self.cargarNivel(lvl)

        def inicialOffset(self, cameraOffset):

            (cameraOffsetX,cameraOffsetY) = cameraOffset

            offsetX =- cameraOffsetX
            offsetY =- cameraOffsetY
            self.background_list[1][1].move_ip(offsetX,offsetY)

            for tile in self.tile_list:
                tile[1].x -= cameraOffsetX
                tile[1].y -= cameraOffsetY

            for platform in self.platform_list:
                platform[1].x -= cameraOffsetX
                platform[1].y -= cameraOffsetY
            
        def draw(self, screen, cameraOffset):
            # Se dibuja las tiles teniendo en cuenta el scroll

            (cameraOffsetX,cameraOffsetY) = cameraOffset

            offsetX =- cameraOffsetX
            offsetY =- cameraOffsetY
            self.background_list[1][1].move_ip(offsetX,offsetY)

            for background in self.background_list:
                #background[1].x -= cameraOffsetX
                #background[1].y -= cameraOffsetY
                screen.blit(background[0], background[1])
            
            

            for tile in self.tile_list:
                tile[1].x -= cameraOffsetX
                tile[1].y -= cameraOffsetY
                screen.blit(tile[0], tile[1])
            
            for platform in self.platform_list:
                platform[1].x -= cameraOffsetX
                platform[1].y -= cameraOffsetY
                screen.blit(platform[0], platform[1])

        def seleccionarTextura(self, fila, columna, maxColumna, altura, anchura, imagen):
            if columna >= maxColumna:
                return self.seleccionarTextura(fila+1, columna-10, maxColumna, altura, anchura, imagen)
            else:
                return imagen.subsurface((columna*anchura, fila*altura, anchura, altura))
            
        def loadMap(self, map, compression, columns, tileHeight, tileWidth, textures, mapWidth):
            
             # Iniciar la posicion del mapa
            mapaX = 0
            mapaY = 0

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
                    
                # Se actualiza la posicion del mapa
                mapaX += 1
                if mapaX >= mapWidth:
                    mapaX = 0
                    mapaY += 1

        def loadPlatforms(self, map, compression, columns, tileHeight, tileWidth, textures, mapWidth):
            
             # Iniciar la posicion del mapa
            mapaX = 0
            mapaY = 0

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
                    self.platform_list.append(tileTuple)

                # Se actualiza la posicion del mapa
                mapaX += 1
                if mapaX >= mapWidth:
                    mapaX = 0
                    mapaY += 1

        def loadEntities(self, map, compression, columns, tileHeight, tileWidth, mapWidth):

            mapaX = 0
            mapaY = 0
            
            for tile in map:
                # Si un tile               

                if tile == 1:
                    pistol = Pistol(mapaX * tileWidth, mapaY * tileHeight)
                    self.gunPickups.add(pistol)
                
                elif tile == 2:
                    shieldPickup = ShieldPickup(mapaX * tileWidth, mapaY * tileHeight)
                    self.gunPickups.add(shieldPickup)

                elif tile == 3:
                    grenadeLauncher = GrenadeLauncher(mapaX * tileWidth, mapaY * tileHeight)
                    self.gunPickups.add(grenadeLauncher)

                elif tile == 4:
                    health = Health(mapaX * tileWidth, mapaY * tileHeight, self.dificulty)
                    self.healthPickUps.add(health)

                elif tile == 6:
                    computer = Computer(mapaX * tileWidth, mapaY * tileHeight, self.enemyFactorySecuence)
                    self.interactiveGroup.add(computer)

                elif tile == 7:
                    en = WallDestructible(mapaX * tileWidth, mapaY * tileHeight,self.destructibleTile_list)
                    self.destructibleTile_list.append(en.rect)
                    self.destructibles_group.add(en)

                elif tile == 8:
                    pistol = PistolUpgrade(mapaX * tileWidth, mapaY * tileHeight)
                    self.gunPickups.add(pistol)

                elif tile == 9:
                    dash = Dash(mapaX * tileWidth, mapaY * tileHeight)
                    self.gunPickups.add(dash)

                # Crear enemigos
                elif tile == 5 or (tile >= 10 and tile <= 15):
                    self.enemyFactory.createEnemy(mapaX * tileWidth, mapaY * tileHeight, tile, self.boss, self.enemies)

                elif tile == 40:
                    trigger = Trigger.Trigger(mapaX*tileWidth, mapaY*tileHeight, tileWidth*6, tileHeight, "lvl1")
                    self.triggerGroup.add(trigger)
                elif tile == 41: 
                    trigger = Trigger.Trigger(mapaX*tileWidth, mapaY*tileHeight, tileWidth, tileHeight*4, "lvl1")
                    self.triggerGroup.add(trigger)
                elif tile == 42:
                    trigger = Trigger.Trigger(mapaX*tileWidth, mapaY*tileHeight, tileWidth*6, tileHeight, "lvl2")
                    self.triggerGroup.add(trigger)
                elif tile == 43: 
                    trigger = Trigger.Trigger(mapaX*tileWidth, mapaY*tileHeight, tileWidth, tileHeight*4, "lvl2")
                    self.triggerGroup.add(trigger)
                elif tile == 44:
                    trigger = Trigger.Trigger(mapaX*tileWidth, mapaY*tileHeight, tileWidth*6, tileHeight, "lvl3")
                    self.triggerGroup.add(trigger)
                elif tile == 45: 
                    trigger = Trigger.Trigger(mapaX*tileWidth, mapaY*tileHeight, tileWidth, tileHeight*4, "lvl3")
                    self.triggerGroup.add(trigger)
                elif tile == 46:
                    trigger = Trigger.Trigger(mapaX*tileWidth, mapaY*tileHeight, tileWidth*6, tileHeight, "lvl4")
                    self.triggerGroup.add(trigger)
                elif tile == 47: 
                    trigger = Trigger.Trigger(mapaX*tileWidth, mapaY*tileHeight, tileWidth, tileHeight*4, "lvl4")
                    self.triggerGroup.add(trigger)
                elif tile == 48:
                    trigger = Trigger.Trigger(mapaX*tileWidth, mapaY*tileHeight, tileWidth, tileHeight*4, "lvl2Vent")
                    self.triggerGroup.add(trigger)
                
                    
                # Se actualiza la posicion del mapa
                mapaX += 1
                if mapaX >= mapWidth:
                    mapaX = 0
                    mapaY += 1
                
        def getPlatformsList(self):
            pList = []
            for platform in self.platform_list:
                pList.append(platform[1])
            return pList
        
        def getTilesList(self):
            tList = []
            for tile in self.tile_list:
                tList.append(tile[1])
            return tList
        
        def getDestructiblesList(self):
            return self.destructibleTile_list
        
        def cargarNivel(self, nivel):
            # Cargar el json con los datos del nivel

            with open(LVLS_PATH + nivel + '/lvlData.json', 'r') as file:
                nivelData = file.read()
            nivelData = json.loads(nivelData)
            levelData = nivelData['layers'][1]
            platforms = nivelData['layers'][2]['data']
            entities = nivelData['layers'][3]['data']
            map = levelData['data']
            mapWidth = levelData['width']
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

            background = pygame.image.load(LVLS_PATH + nivel + '/background.png').convert_alpha()
            spaceBackground = pygame.transform.scale(pygame.image.load(LVLS_PATH + '/space2.jpg'), (SCREEN_WIDTH,SCREEN_HEIGTH)).convert()

            backgroundRect = background.get_rect()
            spaceBackgroundRect = spaceBackground.get_rect()
            spaceBackgroundRect.width = 15
            spaceBackgroundRect.height = 15

            self.background_list.append((spaceBackground, spaceBackgroundRect))
            self.background_list.append((background, backgroundRect))

            self.loadMap(map, compression, columns, tileHeight, tileWidth, textures, mapWidth)
            self.loadPlatforms(platforms, compression, columns, tileHeight, tileWidth, textures, mapWidth)
            self.loadEntities(entities, compression, columns, tileHeight, tileWidth, mapWidth)
        
        def initSecuence(self,enemyFactory,enemies):
            en = enemyFactory.createEnemy()
            self.enemies.add(en)