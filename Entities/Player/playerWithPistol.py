import pygame
from .player import Player
from .PlayerStates.idle import Idle
from .PlayerStates.run import Run
from .PlayerStates.run_shooting import RunShootingRight, RunShootingLeft
from .PlayerStates.jump import Jump
from .PlayerStates.shoot import Shoot
from .playerAbstract import PlayerAbstract
from Entities.bullet import Bullet
from Constants.constants import *

class PlayerWithPistol(PlayerAbstract):
    def __init__(self, player):
        super().__init__(player.position().x, player.position().y, player.getDificulty())
        self.player = player

        # Shoot - Variables disparo
        self.disparosList = []
        self.shootCooldown = self.shootCooldownConst
        #self.velocidadBala = 10
        self.disparoImg = pygame.image.load(PLAYER_PATH + 'lazer_1.png')

        # Imagenes
        self.states = {
            "IDLE": Idle(False),
            "RUNR": Run(True),
            "RUNL": Run(True),
            "RUNSHOOTR": RunShootingRight(),
            "RUNSHOOTL": RunShootingLeft()
        }

        self.anim = 0
        self.state_name = "IDLE"
        self.state = self.states[self.state_name]
        self.standing = self.state.get_initial()
        self.deadImage = pygame.transform.rotate(self.standing,90)
        self.hitImage = pygame.transform.rotate(self.standing,90)
    
    def idle(self):
        self.state.done = True
        self.state.next_state = self.state.posibleNexts["IDLE"]

    def stopShooting(self):
        self.state.done = True
        self.state.next_state = self.state.posibleNexts["STOP-SHOOT"]

    def move_left(self):
        self.player.move_left()
    
    def move_right(self):
        self.player.move_right()
    
    def jump(self):
        self.player.jump()
    
    def getHp(self):
        return self.player.getHp()
    
    def interact(self, interactuableGroup):
        self.player.interact(interactuableGroup)

    def update(self, world, dt, enemies_group, interactuableGroup, cameraOffset):
        cameraOffset = self.player.update(world, dt, enemies_group, interactuableGroup, cameraOffset)
        self.shootCooldown -= 1
        
        for disparo in self.disparosList:
            disparo.update(cameraOffset)
            if disparo.checkBulletCollision(world, enemies_group, self.bulletDamage) or disparo.checkDespawnTime():
                self.disparosList.remove(disparo)
                del disparo
        
        return cameraOffset
            
    def deflect(self, direction, bulletImage, velocidadBala):
        self.player.deflect(direction,bulletImage,velocidadBala)

    def shoot(self, direction):
        self.state.done = True
        self.state.next_state = "RUNSHOOTR"
        if self.shootCooldown <= 0:
            self.shootCooldown = self.shootCooldownConst
            disparo = Bullet(self.disparoImg, direction, self.bulletSpeed, self.player.position().x, self.player.position().y)
            self.disparosList.append(disparo)
            

    def draw(self, screen):
        self.player.draw(screen)

        print(self.disparosList)
        for disparo in self.disparosList:
            disparo.draw(screen)

    def doInteract(self, interactuableGroup):
        self.player.doInteract(interactuableGroup)

    def position(self):
        return self.player.position()
    
    def hit(self, damage):
        return self.player.hit(damage)
    
    def cover(self):
        self.player.cover()

    def heal(self,healingPower):
        self.player.heal(healingPower)

    def launchGrenade(self, direction,grenades_group):
        self.player.launchGrenade(direction,grenades_group)
    
    def getCurrentVelocity(self):
        return self.player.getCurrentVelocity()
    
    def setGrabbed(self, dy,barnacleRect):
        self.player.setGrabbed(dy,barnacleRect)

    def unSetGrabbed(self):
        self.player.unSetGrabbed()