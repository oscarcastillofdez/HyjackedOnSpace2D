import pygame
from .PlayerStates.idle import Idle, IdleShoot
from .PlayerStates.run import Run, RunShoot
from .PlayerStates.jump import Jump, JumpShoot
from math import floor
from Constants.constants import *
from MovementAndCollisions.movement import *
from .playerAbstract import PlayerAbstract
from Entities.shield import Shield
from Entities.grenade import Grenade


class PlayerWithGrenadeLauncher(PlayerAbstract):
        def __init__(self, player,ui):
            print("BBBBBBBBBBBBB")
            super().__init__(player.position().x, player.position().y, player.getDificulty())
            self.player = player

            self.states = {
                "IDLE": Idle(True),
                "RUN": Run(True),
                "JUMP": Jump(True),
                "IDLE-SHOOT": IdleShoot(),
                "JUMP-SHOOT": JumpShoot(),
                "RUN-SHOOT": RunShoot()
            }
            self.anim = 0
            self.state_name = "IDLE"
            self.state = self.states[self.state_name]
            self.standing = self.player.standing
            self.deadImage = pygame.transform.rotate(self.standing,90)
            self.hitImage = pygame.transform.rotate(self.standing,90)

            self.shieldImage = pygame.transform.scale(pygame.image.load(PLAYER_PATH + '/plasma_shield.png'), (150,150))
            self.shieldHitImage = pygame.transform.scale(pygame.image.load(PLAYER_PATH + '/plasma_shield_hit.png'), (150,150))

            self.shield = Shield(self.shieldImage)
            self.applyShield = False

            self.grenadeImg = pygame.image.load(PLAYER_PATH + "grenade.png")
            self.grenadeVelocity = 8
            self.shootCooldown = self.shootCooldownConst

            self.addObserver(ui.uiGrenadeLauncher)
            ui.uiGrenadeLauncher.toggleShow()
        
        def getUiText(self):
            return self.player.getUiText()
        
        def getUiHearts(self):
            return self.player.getUiHearts()

        def move_left(self):
            self.player.move_left()

        def move_right(self):
            self.player.move_right()

        def jump(self):
            self.player.jump()
        
        def stopShooting(self):
            self.player.stopShooting()
        
        def idle(self):
            self.player.idle()

        def getHp(self):
            return self.player.getHp()
        
        def hit(self, damage):
            return self.player.hit(damage)
            
        def getShieldHp(self):
            return self.player.getShieldHp()
        
        def interact(self, interactuableGroup):
            self.player.interact(interactuableGroup)
            
        def getInteractuableText(self):
            return self.player.getInteractuableText()
                
        def update(self, world, dt, enemies_group, interactuableGroup, triggerGroup, cameraOffset) -> tuple:
            self.shootCooldown -= 1 * (dt/100)
            return self.player.update(world, dt, enemies_group, interactuableGroup, triggerGroup, cameraOffset)
        
        def deflect(self, direction, newBulletImage, velocidadBala):
            self.player.deflect(direction, newBulletImage, velocidadBala)
        
        def shootUpdateSprites(self, direction):
            self.player.shootUpdateSprites(direction)

        def shoot(self, direction, bullets_group):
            self.player.shoot(direction,bullets_group)

        def draw(self, screen):
            self.player.draw(screen)

        def position(self):
            return self.player.position()
        
        def cover(self):
            self.player.cover()

        def heal(self,healingPower):
            self.player.heal(healingPower)

        def launchGrenade(self, direction, grenades_group):
            if self.shootCooldown <= 0:
                self.shootCooldown = self.shootGrenadeCooldownConst
                grenade = Grenade(self.grenadeImg, direction, self.grenadeVelocity, self.player.position().x, self.player.position().y, self.grenadeDamage, self, self)
                grenades_group.add(grenade)

        def doInteract(self, interactuableGroup):
            self.player.doInteract(interactuableGroup)    
        
        def setGrabbed(self, dy,barnacleRect):
            self.player.setGrabbed(dy,barnacleRect)

        def unSetGrabbed(self):
            self.player.unSetGrabbed()

        def dash(self):        
            self.player.dash()

        def unDash(self):
            self.player.unDash()
      
        def lookUp(self):
         self.player.lookUp()

        def lookDown(self):
            self.player.lookDown()

        def shakeOn(self):
            self.player.shakeOn()

        def getDashCooldown(self):
            return self.player.getDashCooldown()
        def getHoldDash(self):
            return self.player.getHoldDash()
        def setHoldDash(self, b):
            self.player.setHoldDash(b)
        def setDashing(self, b):
            self.player.setDashing(b)
        def setDashDuration(self, n):
            self.player.setDashDuration(n)
        def setDashCooldown(self, n):
            self.player.setDashCooldown(n)