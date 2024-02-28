import pygame
from playerStates.idle import Idle
from playerStates.run import Run
from math import floor
from global_vars import *
from aux_functions import *

class PlayerAbstract():
    def __init__(self,x,y):
        # Imagenes
        self.states = {
            "IDLE": Idle(False),
            "RUNR": Run(False, False),
            "RUNL": Run(False, True),
            "RUNGL": Run(gun=True,left=True),
            "RUNGR": Run(gun=True, left=False)
        }
        self.current_state = self.states["IDLE"]
        self.anim = 0
        self.standing = self.current_state.get_initial()
        self.deadImage = pygame.transform.rotate(self.standing,90)
        self.hitImage = pygame.transform.rotate(self.standing,90)            # Posicion
        self.rect = self.standing.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.standing.get_width()
        self.height = self.standing.get_height()
        self.velY = 0            # Movimiento
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
        self.hitCooldown = 60            #Armas
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