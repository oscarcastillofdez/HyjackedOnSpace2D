import pygame
from .PlayerStates.idle import Idle
from .PlayerStates.run import RunRight, RunLeft
from .PlayerStates.jump import Jump
from math import floor
from Constants.constants import *
from MovementAndCollisions.aux_functions import *
from .playerAbstract import PlayerAbstract
from Entities.shield import Shield
from Entities.grenade import Grenade


class PlayerWithGrenadeLauncher(PlayerAbstract):
        def __init__(self, player):
            print("BBBBBBBBBBBBB")
            super().__init__(player.position().x, player.position().y)
            self.player = player

            # Imagenes
            self.states = {
                "IDLE": Idle(False),
                "RUNR": RunRight(True),
                "RUNL": RunLeft(True),
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

            self.grenadeImg = pygame.image.load(PLAYER_PATH + "grenade.png")
            self.grenadeVelocity = 5
            self.disparosList = []


        def move_left(self):
            self.player.move_left()

        def move_right(self):
            self.player.move_right()

        def jump(self):
            self.player.jump()

        def getHp(self):
            return self.player.getHp()
        
        def hit(self):
            return self.player.hit()
            
        def getShieldHp(self):
            return self.player.getShieldHp()
        
        def interact(self, interactuableGroup):
            self.player.interact(interactuableGroup)
            
        def getInteractuableText(self):
            return self.player.getInteractuableText()
                
        def update(self, world, dt, enemies_group, interactuableGroup, cameraOffset) -> tuple:
            self.coolDown -= 1
            return self.player.update(world, dt, enemies_group, interactuableGroup, cameraOffset)
        
        def deflect(self, direction, newBulletImage, velocidadBala):
            self.player.deflect(direction, newBulletImage, velocidadBala)

        def shoot(self, direction):
            self.player.shoot(direction)

        def draw(self, screen):
            self.player.draw(screen)

        def position(self):
            return self.player.position()
        
        def cover(self):
            self.player.cover()

        def heal(self):
            self.player.heal()

        def launchGrenade(self, direction, grenades_group):
            if self.coolDown <= 0:
                self.coolDown = 30
                grenade = Grenade(self.grenadeImg, direction, self.grenadeVelocity, self.player.position().x, self.player.position().y)
                grenades_group.add(grenade)

        def doInteract(self, interactuableGroup):
            self.player.doInteract(interactuableGroup)    