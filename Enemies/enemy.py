import pygame
from Constants.global_vars import *
from Enemies.entity import Entity
import math

class Enemy(pygame.sprite.Sprite, Entity):
    def __init__(self,x,y,globalVars):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('Assets/img/pj.png'), (120, 120))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 100
        self.patrollingchasingSpeed = 1
        
        self.moved = 0
        self.globalVars = globalVars
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.inAir = True
        self.velY = 0
        self.chasingSpeed = 4
        self.jumped = False
        self.jumpDelay = 0
        self.viewDirection = 1
        self.chaseTime = 120
        
        # Define los estados posibles
        self.states = {"patrolling": self.patrol,
                       "chasing": self.chase,
                       "attacking": self.attack}
        
        # Inicializa el estado actual
        self.current_state = "patrolling"
        self.visionLine = pygame.Rect(self.rect.centerx, self.rect.y, 500, 50) 
    
    def update(self, world, player):
        # Llama a la función correspondiente al estado actual
        
        self.states[self.current_state](world, player)
        self.player_in_sight(world, player)

    def patrol(self, world, player):
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
        
        # Se calculan las colisiones en ambos ejes
        for tile in world.terrainHitBoxList:
            if tile.colliderect(self.rect.x + self.patrollingchasingSpeed, self.rect.y, self.width, self.height):
                self.patrollingchasingSpeed = -self.patrollingchasingSpeed
                self.viewDirection = -self.viewDirection
            
            if tile.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.velY < 0: #Saltando
                        dy = tile.bottom - self.rect.top
                        self.velY = 0
                    elif self.velY >= 0: #Cayendo
                        dy = tile.top - self.rect.bottom
                        self.velY = 0
                        self.inAir = False

        self.rect.x += self.patrollingchasingSpeed - self.globalVars.CAMERA_OFFSET_X
        self.rect.y += dy - self.globalVars.CAMERA_OFFSET_Y
    
    def chase(self, world, player):
        self.jumpDelay -= 1
        self.chaseTime -= 1

        if self.chaseTime <= 0:
            self.change_state("patrolling")
            
        dy = 0
        self.moved = 0

        if player.position().x > self.rect.x:
            self.viewDirection = 1
            self.moved -= self.chasingSpeed

        if player.position().x < self.rect.x:
            self.viewDirection = -1
            self.moved += self.chasingSpeed

        #if player.position.x == self.rect.x and player.position.y < self.rect.y:
            # Buscar otro camino (cambiar a un estado pathfinding? 
            # Mover x bloques hacia un lado hasta encontrar una pared que no puede saltar o conseguir bajar la y)
            # Si se encuentra una pared que no puede saltar cambia de direccion 
            # Puede quedar atascado, alejarse inecesariamente o caerse al vacio
            
        self.inAir = True
        self.velY += 1
        if self.velY > 10:
            self.velY = 1
        
        dy += self.velY

        for tile in world.terrainHitBoxList:
            if tile.colliderect(self.rect.x - self.moved, self.rect.y, self.width, self.height):
                if self.jumpDelay <= 0:
                    self.jumpDelay = 50
                    self.velY = -12
                    dy = self.velY

                self.moved = 0
            
            if tile.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.velY < 0: #Saltando
                        dy = tile.bottom - self.rect.top
                        self.velY = 0
                    elif self.velY >= 0: #Cayendo
                        dy = tile.top - self.rect.bottom
                        self.velY = 0
                        self.inAir = False
        
            

        self.rect.x -= self.globalVars.CAMERA_OFFSET_X
        self.rect.y += dy - self.globalVars.CAMERA_OFFSET_Y
        
        self.rect.x -= self.moved

        if self.rect.colliderect(player.position()):
            self.change_state("attacking")
        
    
    def attack(self, world, player):
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