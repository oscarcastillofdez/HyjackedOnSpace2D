import pygame
from .PlayerStates.idle import Idle
from .PlayerStates.run import RunRight, RunLeft
from .PlayerStates.jump import Jump
from math import floor
from Constants.constants import *
from MovementAndCollisions.aux_functions import *
from .playerAbstract import PlayerAbstract
from Entities.shield import Shield
from Entities.bullet import Bullet


class PlayerWithShield(PlayerAbstract):
        def __init__(self, player):
            print("BBBBBBBBBBBBB")
            super().__init__(player.position().x, player.position().y)
            self.player = player

            # Imagenes
            self.states = {
                "IDLE": Idle(False),
                "RUNR": RunRight(False, False),
                "RUNL": RunLeft(False, True),
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
            self.coolDown = 30

            self.deflectedShotsList = []


        def move_left(self):
            self.player.move_left()

        def move_right(self):
            self.player.move_right()

        def jump(self):
            self.player.jump()

        def getHp(self):
            return self.player.getHp()
        
        def hit(self):
            if not self.applyShield:
                return self.player.hit()
            else:
                self.shield.deflect(self.shieldHitImage)
                self.notify()
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
                
        def update(self, world, dt, enemies_group, interactuableGroup, cameraOffset) -> tuple:
            cameraOffset = self.player.update(world, dt, enemies_group, interactuableGroup, cameraOffset)
            self.coolDown -= 1

            for shot in self.deflectedShotsList:
                shot.update(cameraOffset)
                if shot.checkBulletCollision(world, enemies_group) or shot.checkDespawnTime():
                    self.deflectedShotsList.remove(shot)
                    del shot

            self.shield.update(self)

            return cameraOffset


        def checkGunPick(self, world):
            return self.player.checkGunPick(world)
        
        def deflect(self, direction, newBulletImage, velocidadBala):
            if self.coolDown <= 0:
                self.coolDown = 30
                disparo = Bullet(newBulletImage, direction, velocidadBala, self.player.position().x, self.player.position().y)
                self.deflectedShotsList.append(disparo)

        def shoot(self, direction):
            self.player.shoot(direction)

        def draw(self, screen):
            self.player.draw(screen)
            if self.applyShield:
                self.shield.draw(screen)
                self.applyShield = False
            for disparo in self.deflectedShotsList:
                disparo.draw(screen)

        def position(self):
            return self.player.position()
        
        def cover(self):
            self.applyShield = True

            


            