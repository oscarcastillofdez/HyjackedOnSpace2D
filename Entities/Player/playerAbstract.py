import pygame
from PlayerStates.idle import Idle
from PlayerStates.run import Run
from math import floor
from Constants.global_vars import *
from MovementAndCollisions.aux_functions import *

class PlayerAbstract():
    def __init__(self,x,y):
        # Posicion
        self.rect = pygame.Rect(0,0,66,94)
        self.rect.x = x
        self.rect.y = y
        self.width = self.rect.width
        self.height = self.rect.height
        
        # Movimiento
        self.velY = 0            
        self.inAir = True
        self.moving_left = False
        self.moving_right = False
        self.left_mov = 0
        self.right_mov = 0
        self.jumping = False
        self.hold_jump = False
        self.pressed_jump = 0
        
        #Vida
        self.healthPoints = 3
        self.hitCooldown = 60
        
        #Armas
        self.arma = None
        self.uiElementsList = []
        self.interactuableText = ""

    def move_left(self):
        pass
    
    def move_right(self):
        pass
    
    def jump(self):
        pass
    
    def getHp(self):
        pass
    
    def checkHit(self, enemies_group):
        pass
    
    def update(self, world, globalVars, dt):
        pass
    
    def shoot(self, direction, gv):
        pass
    
    def draw(self, screen):
        pass

    def checkGunPick(self, world):
        pass
    
    def addObserver():
        pass
    
    def delObserver():
        pass
    
    def notify():
        pass
    
    def position():
        pass