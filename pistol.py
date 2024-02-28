import pygame
from playerStates.idle import Idle
from playerStates.run import Run
from playerStates.jump import Jump
from playerStates.shoot import Shoot
from playerAbstract import PlayerAbstract
from player import Player
from bullet import Bullet

class Pistol(PlayerAbstract):
    def __init__(self, player):
        # Imagenes
        self.states = {
            "IDLE": Idle(False),
            "RUNR": Run(True, False),
            "RUNL": Run(True, True),
            "JUMP": Jump(),
            "shoot-left": Shoot("left"),
            "shoot-up": Shoot("up"),
            "shoot-right": Shoot("right"),
            "shoot-down": Shoot("down"),
        }
        self.anim = 0
        self.current_state = self.states["IDLE"]
        self.standing = self.current_state.get_initial()
        self.deadImage = pygame.transform.rotate(self.standing,90)
        self.hitImage = pygame.transform.rotate(self.standing,90)    

        self.player = player # Clase base player

        self.disparosList = []
        self.coolDown = 30
        self.velocidadBala = 10
        
        self.disparoImg = pygame.image.load('Assets/img/lazer_1.png')

    def move_left(self):
        self.current_state = self.states["RUNL"]
        self.player.moving_left = True
    
    def move_right(self):
        self.current_state = self.states["RUNR"]
        self.player.moving_right = True
    
    def jump(self):
        self.current_state = self.states["JUMP"]
        self.player.jump()
    
    def getHp(self):
        return self.player.getHp()
    
    def update(self, world, globalVars, dt, enemies_group, interactuableGroup):
        self.player.update(world, globalVars, dt, enemies_group)
        self.coolDown -= 1
        
        for disparo in self.disparosList:
            disparo.update()
            if disparo.checkBulletCollision(world, enemies_group) or disparo.checkDespawnTime():
                self.disparosList.remove(disparo)
                del disparo
            

    def shoot(self, direction, gv):
        self.current_state = self.states[f"shoot-{direction}"]
        if self.coolDown <= 0:
            self.coolDown = 30

            disparo = Bullet(self.disparoImg, direction, self.velocidadBala, self.player.rect.x, self.player.rect.y, gv)
            self.disparosList.append(disparo)

    def draw(self, screen):
        """if self.player.inAir:
            self.current_state = self.states["JUMP"]"""
        if self.anim > 6:
                self.standing = self.current_state.next_sprite()
                self.anim = 0
        self.anim += 1
        for disparo in self.disparosList:
            disparo.draw(screen)
        screen.blit(self.standing, (self.player.rect.x-20,self.player.rect.y,self.player.rect.width,self.player.rect.height))

    def checkGunPick(self, world):
        return self.player.checkGunPick(world)
    
    def position(self):
        return self.player.position()
    
    def hit(self):
        return self.player.hit()