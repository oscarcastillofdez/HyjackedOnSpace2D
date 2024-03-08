import pygame
from Constants.constants import *
from Entities.bullet import Bullet
from Game.collisionHandler import CollisionHandler
from .entity import Entity
from Game.spritesheet import Spritesheet
import math
import random

class ShooterEnemy(pygame.sprite.Sprite, Entity):
    def __init__(self,x,y,onlyChase):
        pygame.sprite.Sprite.__init__(self)
        # Otros objetos
        self.collisionHandler = CollisionHandler()

        # Atributos de posicion e imagen
        self.image = pygame.transform.scale(pygame.image.load(ENEMIES_PATH + 'Box.png'), (64,64))
        # self.sprites = Spritesheet('Assets/Images/Entities/enemy trooper_walk.png',(120,120)).cargar_sprites(512,64)
        # self.image = self.sprites[0]
        # self.time = 0
        # self.index = 0

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Atributos de movimiento
        self.moved = 0
        self.velY = 0
        self.jumpDelay = 0
        self.patrollingSpeed = 1
        self.chasingSpeed = random.randint(2, 4)

        # Atributos de control de vision
        self.visionLine = pygame.Rect(self.rect.centerx, self.rect.y, 500, 50) 
        self.viewDirection = 1
        self.minAtackDistance = 300 # Distancia directa hacia el jugador (diagonal)
        self.distanciaAlJugador = 0

        # Atributos de control de disparo
        self.shootCooldown = 60
        self.disparosList = []
        self.disparoImg = pygame.image.load('Assets/Images/Entities/Player/lazer_24.png')
        self.angle = 0
        self.velocidadBala = 10



        # Atributos de control de estados
        self.chaseTime = 120
        self.onlyChase = onlyChase
        self.states = {"patrolling": self.patrol,
                       "chasing": self.chase,
                       "attacking": self.attack,
                       "die": self.die}
        self.current_state = "patrolling"
        if onlyChase:
            self.current_state = "chasing"

        
    def checkBulletCollision2(self, world, player, disparo):
        if disparo.bulletPosition().colliderect(player.position()):
            if player.hit():
                return True
            else:
                #player.deflect(self.angle + 180, self.disparoImg, self.velocidadBala)
                return True
            
        tileHitBoxList = world.getTilesList()
        destructibleHitBoxList = world.getDestructiblesList()
        
        tileIndex = disparo.bulletPosition().collidelist(tileHitBoxList)

        destructibleIndex = disparo.bulletPosition().collidelist(destructibleHitBoxList)
        
        if tileIndex >= 0 or destructibleIndex >= 0:
            return True
        

    def update(self, dt, world, player,cameraOffset, enemies_group):
        # self.time += dt
        # if self.time > 100:
        #     self.index += 1
        #     if self.index >= len(self.sprites):
        #         self.index=0
        #     self.image = self.sprites[self.index]

        for disparo in self.disparosList:
            disparo.update(cameraOffset)
            if self.checkBulletCollision2(world, player, disparo) or disparo.checkDespawnTime():
                self.disparosList.remove(disparo)
                del disparo

        self.states[self.current_state](world, player, cameraOffset,enemies_group)
        self.player_in_sight(world, player)

    def player_in_sight(self, world, player):
        dx = player.position().centerx - self.rect.centerx
        dy = player.position().centery - self.rect.centery

        self.distanciaAlJugador = math.sqrt((dx**2) + (dy**2))
        self.angle = -math.degrees(math.atan2(dy, dx))

        if self.viewDirection == 1:
            self.visionLine.x = self.rect.centerx
            self.visionLine.y = self.rect.y
        else:
            self.visionLine.x = self.rect.centerx - 500
            self.visionLine.y = self.rect.y

        if self.visionLine.colliderect(player.position()) and self.current_state != "attacking":
            self.chaseTime = 120
            self.current_state = "chasing"
    
    def patrol(self,world, player,cameraOffset,enemies_group):
        # Comportamiento cuando está patrullando
        dy = 0

        self.moved += 1
        if self.moved >= 400:
            self.viewDirection = -self.viewDirection
            self.patrollingSpeed = -self.patrollingSpeed
            self.moved = 0

        self.velY += 1
        if self.velY > 10:
             self.velY = 10
        dy += self.velY

        tileHitBoxList = world.getTilesList()
        platformHitBoxList = world.getPlatformsList()
        destructibleHitBoxList = world.getDestructiblesList()

        tileCollisions = self.collisionHandler.checkCollisions(self, tileHitBoxList, self.patrollingSpeed, dy)
        platformCollisions = self.collisionHandler.checkCollisions(self, platformHitBoxList, self.patrollingSpeed, dy)
        destructibleCollisions = self.collisionHandler.checkCollisions(self, destructibleHitBoxList, self.patrollingSpeed, dy)

        if tileCollisions[0] >= 0 or destructibleCollisions[0] >= 0:
            self.patrollingSpeed = -self.patrollingSpeed
            self.viewDirection = -self.viewDirection

        if tileCollisions[1] >= 0:
            if self.velY < 0: #Saltando
                dy = tileHitBoxList[tileCollisions[1]].bottom - self.rect.top
                self.velY = 0
            elif self.velY >= 0: #Cayendo
                dy = tileHitBoxList[tileCollisions[1]].top - self.rect.bottom
                self.velY = 0

        if destructibleCollisions[1] >= 0:
            if self.velY < 0: #Saltando
                dy = destructibleHitBoxList[destructibleCollisions[1]].bottom - self.rect.top
                self.velY = 0
            elif self.velY >= 0: #Cayendo
                dy = destructibleHitBoxList[destructibleCollisions[1]].top - self.rect.bottom
                self.velY = 0

        if platformHitBoxList[platformCollisions[0]].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
            if self.velY >= 0 and (self.rect.bottom - platformHitBoxList[platformCollisions[0]].top) < 10: #Cayendo
                dy = platformHitBoxList[platformCollisions[0]].top - self.rect.bottom
                self.velY = 0
        
        self.rect.x += self.patrollingSpeed - cameraOffset[0]
        self.rect.y += dy - cameraOffset[1]
    
    def chase(self,world, player,cameraOffset,enemies_group):
        self.jumpDelay -= 1
        self.chaseTime -= 1

        if self.chaseTime <= 0 and not self.onlyChase:
            self.current_state = "patrolling"
            
        dy = 0
        self.moved = 0


        if player.position().x > self.rect.x:
            self.viewDirection = 1
            self.moved -= self.chasingSpeed

        if player.position().x < self.rect.x:
            self.viewDirection = -1
            self.moved += self.chasingSpeed

        self.velY += 1
        if self.velY > 10:
            self.velY = 1
        
        dy += self.velY

        tileHitBoxList = world.getTilesList()
        platformHitBoxList = world.getPlatformsList()
        destructibleHitBoxList = world.getDestructiblesList()

        tileCollisions = self.collisionHandler.checkCollisions(self, tileHitBoxList, self.patrollingSpeed, dy)
        platformCollisions = self.collisionHandler.checkCollisions(self, platformHitBoxList, self.patrollingSpeed, dy)
        destructibleCollisions = self.collisionHandler.checkCollisions(self, destructibleHitBoxList, self.patrollingSpeed, dy)

        if tileCollisions[0] >= 0 or destructibleCollisions[0] >= 0:
            if self.jumpDelay <= 0:
                self.jumpDelay = 50
                self.velY = -12
                dy = self.velY

            self.moved = 0

        if tileCollisions[1] >= 0:
            if self.velY < 0: #Saltando
                dy = tileHitBoxList[tileCollisions[1]].bottom - self.rect.top
                self.velY = 0
            elif self.velY >= 0: #Cayendo
                dy = tileHitBoxList[tileCollisions[1]].top - self.rect.bottom
                self.velY = 0

        if destructibleCollisions[1] >= 0:
            if self.velY < 0: #Saltando
                dy = destructibleHitBoxList[destructibleCollisions[1]].bottom - self.rect.top
                self.velY = 0
            elif self.velY >= 0: #Cayendo
                dy = destructibleHitBoxList[destructibleCollisions[1]].top - self.rect.bottom
                self.velY = 0

        if platformHitBoxList[platformCollisions[0]].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
            if self.velY >= 0 and (self.rect.bottom - platformHitBoxList[platformCollisions[0]].top) < 10: #Cayendo
                dy = platformHitBoxList[platformCollisions[0]].top - self.rect.bottom
                self.velY = 0

        self.rect.x -= cameraOffset[0]
        self.rect.y += dy - cameraOffset[1]
        
        self.rect.x -= self.moved

        if self.distanciaAlJugador < self.minAtackDistance:
            self.current_state = "attacking"
    
    def attack(self,world, player,cameraOffset,enemies_group):
        # Disparar cada x segundos
        self.shootCooldown -= 1
        if self.shootCooldown <= 0:
            self.shootCooldown = 30
            disparo = Bullet(self.disparoImg, self.angle, self.velocidadBala, self.rect.x, self.rect.y)
            self.disparosList.append(disparo)

        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]

        if self.distanciaAlJugador > self.minAtackDistance:
            self.current_state = "chasing"

    def drawBullets(self, screen):
        for disparo in self.disparosList:
            disparo.draw(screen)

    def die(self,world, player,cameraOffset,enemies_group):
        enemies_group.remove(self)

    def kill(self):
        self.current_state = "die"  