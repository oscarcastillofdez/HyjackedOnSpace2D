import pygame
from Player.player import Player
from PlayerStates.idle import Idle
from PlayerStates.run import Run
from PlayerStates.jump import Jump
from PlayerStates.shoot import Shoot
from Player.playerAbstract import PlayerAbstract
from bullet import Bullet

class Pistol(PlayerAbstract):
    def __init__(self, player):
        self.player = player

        # Shoot - Variables disparo
        self.disparosList = []
        self.coolDown = 30
        self.velocidadBala = 10
        self.disparoImg = pygame.image.load('Assets/img/lazer_1.png')

        # Imagenes
        self.states = {
            "IDLE": Idle(False),
            "RUNR": Run(False, False),
            "RUNL": Run(False, True),
        }

        self.anim = 0
        self.current_state = self.states["IDLE"]
        self.standing = self.current_state.get_initial()
        self.deadImage = pygame.transform.rotate(self.standing,90)
        self.hitImage = pygame.transform.rotate(self.standing,90)

    def move_left(self):
        self.player.move_left()
    
    def move_right(self):
        self.player.move_right()
    
    def jump(self):
        self.player.jump()
    
    def getHp(self):
        return self.player.getHp()
    
    def update(self, world, globalVars, dt, enemies_group, interactuableGroup):
        self.player.update(world, globalVars, dt, enemies_group, interactuableGroup)
        self.coolDown -= 1
        
        for disparo in self.disparosList:
            disparo.update()
            if disparo.checkBulletCollision(world, enemies_group) or disparo.checkDespawnTime():
                self.disparosList.remove(disparo)
                del disparo
            

    def shoot(self, direction, gv):
        if self.coolDown <= 0:
            self.coolDown = 30

            disparo = Bullet(self.disparoImg, direction, self.velocidadBala, self.player.rect.x, self.player.rect.y, gv)
            self.disparosList.append(disparo)

    def draw(self, screen):
        self.player.draw(screen)

        for disparo in self.disparosList:
            disparo.draw(screen)

    def checkGunPick(self, world):
        return self.player.checkGunPick(world)
    
    def position(self):
        return self.player.position()
    
    def hit(self):
        return self.player.hit()