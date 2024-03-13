import pygame
from .PlayerStates.idle import Idle
from .PlayerStates.run import Run
from .PlayerStates.jump import Jump
from math import floor
from Constants.constants import *
from MovementAndCollisions.movement import *
from .playerAbstract import PlayerAbstract
from Entities.shield import Shield
from Entities.bullet import Bullet


class PlayerWithShield(PlayerAbstract):
        def __init__(self, player, ui):
            super().__init__(player.position().x, player.position().y,player.getDificulty())
            self.player = player

            # Imagenes
            self.states = {
                "IDLE": Idle(False),
                "RUNR": Run(True),
                "RUNL": Run(True),
            }
            # Imagenes
            self.anim = 0 
            self.current_state = self.states["IDLE"]
            self.standing = self.current_state.get_initial()
            self.deadImage = pygame.transform.rotate(self.standing,90)
            self.hitImage = pygame.transform.rotate(self.standing,90)

            self.shieldImage = pygame.transform.scale(pygame.image.load(PLAYER_PATH + '/plasma_shield.png'), (150,150))
            self.shieldHitImage = pygame.transform.scale(pygame.image.load(PLAYER_PATH + '/plasma_shield_hit.png'), (150,150))

            self.shield = Shield(self.shieldImage)
            self.applyShield = False

            self.deflectedShotsList = []
            self.shield.addObserver(ui.uiEnergy)
            ui.uiEnergy.show()

        def idle(self):
            self.player.idle()

        def stopShooting(self):
            self.player.stopShooting()

        def move_left(self):
            self.player.move_left()

        def move_right(self):
            self.player.move_right()

        def jump(self):
            self.player.jump()

        def getHp(self):
            return self.player.getHp()
        
        def hit(self, damage):
            if not self.applyShield or self.shield.getShieldHp() <= 0:
                return self.player.hit(damage)
            else:
                self.shield.deflect(self.shieldHitImage)
                
                return False
            
        def getShieldHp(self):
            return self.shield.getShieldHp()
        
        # La clase checkGunClollide deberia de eliminarse
        # Interact deberia de valer para todo objeto interactuable (Ordenador, puertas, luces, armas, vidas, mejoras...)
        # En world meter armas como un interactuable pygame.sprite.interacutableGroup
        def interact(self, interactuableGroup):
            self.player.interact(interactuableGroup)
            
        def getInteractuableText(self):
            return self.player.getInteractuableText()
                
        def update(self, world, dt, enemies_group, interactuableGroup, triggerGroup, cameraOffset) -> tuple:
            cameraOffset = self.player.update(world, dt, enemies_group, interactuableGroup, triggerGroup, cameraOffset)

            self.shield.update(self)

            return cameraOffset

        def deflect(self, direction, bulletImage, velocidadBala, damage, posx, posy, bullets_group):
            disparo = Bullet(bulletImage, direction, damage, velocidadBala, posx, posy, self, self, True)
            bullets_group.add(disparo)

        def shootUpdateSprites(self, direction):
            self.player.shootUpdateSprites(direction)
            
        def shoot(self, direction, bullets_group):
            self.player.shoot(direction,bullets_group)

        def draw(self, screen):
            self.player.draw(screen)
            if self.applyShield:
                self.shield.draw(screen)
                self.applyShield = False

        def position(self):
            return self.player.position()
        
        def cover(self):
            self.applyShield = True

        def heal(self,healingPower):
            self.player.heal(healingPower)
            
        def launchGrenade(self, direction, grenades_group):
            self.player.launchGrenade(direction, grenades_group)

        def getCurrentVelocity(self):
            return self.player.getCurrentVelocity()
        
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