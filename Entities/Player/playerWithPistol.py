import pygame
from .player import Player
from .PlayerStates.idle import Idle, IdleShoot
from .PlayerStates.run import Run, RunShoot, RunShootDiagUp, RunShootDiagDown, RunShootDown, RunShootUp
from .PlayerStates.jump import Jump, JumpShoot
from .playerAbstract import PlayerAbstract
from Entities.bullet import Bullet
from Constants.constants import *

class PlayerWithPistol(PlayerAbstract):
    def __init__(self, player):
        super().__init__(player.position().x, player.position().y, player.getDificulty())
        self.player = player

        self.shootCooldown = self.shootCooldownConst
        self.disparoImg = pygame.image.load(PLAYER_PATH + 'lazer_1.png')

        # Imagenes
        self.states = {
            "IDLE": Idle(True),
            "RUN": Run(True),
            "JUMP": Jump(True),
            "IDLE-SHOOT": IdleShoot(),
            "JUMP-SHOOT": JumpShoot(),
            "RUN-SHOOT": RunShoot()
        }
        """
            "IDLE": Idle(False),
            "RUN": Run(True),
            "RUN-SHOOT": RunShoot(),
            "RUN-SHOOT-DIAG-UP": RunShootDiagUp(),
            "RUN-SHOOT-DIAG-DOWN": RunShootDiagDown(),
            "RUN-SHOOT-DOWN": RunShootDown(),
            "RUN-SHOOT-UP" : RunShootUp(),
            "IDLE-SHOOT": IdleShoot(),
            "IDLE-SHOOT-UP": IdleShoot(),
            "IDLE-SHOOT-DOWN": IdleShoot(),
            "IDLE-SHOOT-DIAG-UP": IdleShoot(),
            "IDLE-SHOOT-DIAG-DOWN": IdleShoot(),
            "JUMP-SHOOT": JumpShoot(),
            "JUMP": Jump(True)
        """

        self.anim = 0
        self.state_name = "IDLE"
        self.state = self.states[self.state_name]
        self.standing = self.state.get_initial()
        self.deadImage = pygame.transform.rotate(self.standing,90)
        self.hitImage = pygame.transform.rotate(self.standing,90)
    

    def idle(self):
        self.player.state.done = True
        self.player.state.next_state = self.player.state.posibleNexts["IDLE"]

    def stopShooting(self):
        self.player.direction == None
        self.player.state.done = True
        self.player.state.next_state = self.player.state.posibleNexts["STOP-SHOOT"]
        pass

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

    def update(self, world, dt, enemies_group, interactuableGroup, triggerGroup, cameraOffset):
        cameraOffset = self.player.update(world, dt, enemies_group, interactuableGroup, triggerGroup, cameraOffset)
        self.shootCooldown -= 1
        
        return cameraOffset
            
    def deflect(self, direction, bulletImage, velocidadBala):
        self.player.deflect(direction,bulletImage,velocidadBala)

    def shoot(self, direction, bullets_group):
        self.player.direction = direction
        self.player.state.done = True
        self.player.state.next_state = self.player.state.posibleNexts["SHOOT"]

        if self.shootCooldown <= 0:
            self.shootCooldown = self.shootCooldownConst
            disparo = Bullet(self.disparoImg, direction, self.bulletDamage, self.bulletSpeed, self.player.position().centerx - 40, self.player.position().top - 40, self, self)
            bullets_group.add(disparo)
            

    def draw(self, screen):
        self.player.draw(screen)

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