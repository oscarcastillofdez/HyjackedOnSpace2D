import pygame
from Constants.constants import *
from .entity import Entity
from Game.spritesheet import Spritesheet
import math
import random

class Enemy(pygame.sprite.Sprite, Entity):
    def __init__(self,x,y, onlyChase):
        pygame.sprite.Sprite.__init__(self)
        self.onlyChase = onlyChase
        self.time = 0
        self.sprites = Spritesheet('Assets/Images/Entities/enemy trooper_walk.png',(120,120)).cargar_sprites(512,64)
        self.image = self.sprites[0]
        self.index = 0

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 100
        self.patrollingchasingSpeed = 1
        
        self.moved = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.inAir = True
        self.velY = 0
        self.chasingSpeed = random.randint(2, 4)
        self.jumped = False
        self.jumpDelay = 0
        self.viewDirection = 1
        self.chaseTime = 120
        
        # Define los estados posibles
        self.states = {"patrolling": self.patrol2,
                       "chasing": self.chase2,
                       "attacking": self.attack2}
        
        # Inicializa el estado actual
        #self.current_state = self.states["patrolling"]
        self.current_state = "patrolling"

        if onlyChase:
            self.current_state = "chasing"
            
        self.visionLine = pygame.Rect(self.rect.centerx, self.rect.y, 500, 50) 
    
    def update(self, dt, world, player,cameraOffset):
        self.time += dt
        if self.time > 100:
            self.index += 1
            if self.index >= len(self.sprites):
                self.index=0
            self.image = self.sprites[self.index]

        # Llama a la función correspondiente al estado actual
        self.states[self.current_state](world, player,cameraOffset)
        self.player_in_sight(world, player)

    def patrol2(self, world, player,cameraOffset):
        # Comportamiento cuando está patrullando
        dy = 0

        self.inAir = True
        self.moved += 1
        if self.moved >= 400:
            self.viewDirection = -self.viewDirection
            self.patrollingchasingSpeed = -self.patrollingchasingSpeed
            self.moved = 0

        self.velY += 1
        if self.velY > 10:
             self.velY = 10
        dy += self.velY

        tileHitBoxList = world.getTilesList()
        platformHitBoxList = world.getPlatformsList()
        destructibleHitBoxList = world.getDestructiblesList()

        auxRect = pygame.Rect(self.rect.x + self.patrollingchasingSpeed, self.rect.y, self.width, self.height)
        auxRect2 = pygame.Rect(self.rect.x, self.rect.y + dy, self.width, self.height)
        
        tileIndex = auxRect.collidelist(tileHitBoxList)
        tileIndex2 = auxRect2.collidelist(tileHitBoxList)

        platformIndex = auxRect.collidelist(platformHitBoxList)

        destructibleIndex = auxRect.collidelist(destructibleHitBoxList)
        destructibleIndex2 = auxRect2.collidelist(destructibleHitBoxList)

        if tileIndex >= 0 or destructibleIndex >= 0:
            self.patrollingchasingSpeed = -self.patrollingchasingSpeed
            self.viewDirection = -self.viewDirection

        if tileIndex2 >= 0:
            if self.velY < 0: #Saltando
                dy = tileHitBoxList[tileIndex2].bottom - self.rect.top
                self.velY = 0
            elif self.velY >= 0: #Cayendo
                dy = tileHitBoxList[tileIndex2].top - self.rect.bottom
                self.velY = 0
                self.inAir = False

        if destructibleIndex2 >= 0:
            if self.velY < 0: #Saltando
                dy = destructibleHitBoxList[destructibleIndex2].bottom - self.rect.top
                self.velY = 0
            elif self.velY >= 0: #Cayendo
                dy = destructibleHitBoxList[destructibleIndex2].top - self.rect.bottom
                self.velY = 0
                self.inAir = False

        if platformHitBoxList[platformIndex].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
            if self.velY >= 0 and (self.rect.bottom - platformHitBoxList[platformIndex].top) < 10: #Cayendo
                dy = platformHitBoxList[platformIndex].top - self.rect.bottom
                self.velY = 0
                self.inAir = False

        self.rect.x += self.patrollingchasingSpeed - cameraOffset[0]
        self.rect.y += dy - cameraOffset[1]
    
    def chase2(self, world, player,cameraOffset):
        self.jumpDelay -= 1
        self.chaseTime -= 1

        if self.chaseTime <= 0 and not self.onlyChase:
            self.change_state("patrolling")
            
        dy = 0
        self.moved = 0

        if player.position().x > self.rect.x:
            self.viewDirection = 1
            self.moved -= self.chasingSpeed

        if player.position().x < self.rect.x:
            self.viewDirection = -1
            self.moved += self.chasingSpeed

        self.inAir = True
        self.velY += 1
        if self.velY > 10:
            self.velY = 1
        
        dy += self.velY

        tileHitBoxList = world.getTilesList()
        platformHitBoxList = world.getPlatformsList()
        destructibleHitBoxList = world.getDestructiblesList()

        auxRect = pygame.Rect(self.rect.x + self.patrollingchasingSpeed, self.rect.y, self.width, self.height)
        auxRect2 = pygame.Rect(self.rect.x, self.rect.y + dy, self.width, self.height)
        
        tileIndex = auxRect.collidelist(tileHitBoxList)
        tileIndex2 = auxRect2.collidelist(tileHitBoxList)

        platformIndex = auxRect.collidelist(platformHitBoxList)

        destructibleIndex = auxRect.collidelist(destructibleHitBoxList)
        destructibleIndex2 = auxRect2.collidelist(destructibleHitBoxList)

        if tileIndex >= 0 or destructibleIndex >= 0:
            if self.jumpDelay <= 0:
                self.jumpDelay = 50
                self.velY = -12
                dy = self.velY

            self.moved = 0

        if tileIndex2 >= 0:
            if self.velY < 0: #Saltando
                dy = tileHitBoxList[tileIndex2].bottom - self.rect.top
                self.velY = 0
            elif self.velY >= 0: #Cayendo
                dy = tileHitBoxList[tileIndex2].top - self.rect.bottom
                self.velY = 0
                self.inAir = False

        if destructibleIndex2 >= 0:
            if self.velY < 0: #Saltando
                dy = destructibleHitBoxList[destructibleIndex2].bottom - self.rect.top
                self.velY = 0
            elif self.velY >= 0: #Cayendo
                dy = destructibleHitBoxList[destructibleIndex2].top - self.rect.bottom
                self.velY = 0
                self.inAir = False

        if platformHitBoxList[platformIndex].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
            if self.velY >= 0 and (self.rect.bottom - platformHitBoxList[platformIndex].top) < 10: #Cayendo
                dy = platformHitBoxList[platformIndex].top - self.rect.bottom
                self.velY = 0
                self.inAir = False

        self.rect.x -= cameraOffset[0]
        self.rect.y += dy - cameraOffset[1]
        
        self.rect.x -= self.moved

        if self.rect.colliderect(player.position()):
            self.change_state("attacking")
    
    def attack2(self, world, player,cameraOffset):
        player.hit()
    
    # Método para cambiar de estado
    def change_state(self, new_state):
        self.current_state = new_state

    # Lógica para determinar si el jugador está dentro del rango de visión
    def player_in_sight(self, world, player):
        if self.viewDirection == 1:
            self.visionLine.x = self.rect.centerx
            self.visionLine.y = self.rect.y
        else:
            self.visionLine.x = self.rect.centerx - 500
            self.visionLine.y = self.rect.y

        if self.visionLine.colliderect(player.position()):
            self.chaseTime = 120
            self.change_state("chasing")