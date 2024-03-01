import pygame
from .PlayerStates.idle import Idle
from .PlayerStates.run import Run
from .PlayerStates.jump import Jump
from math import floor
from Constants.constants import *
from MovementAndCollisions.aux_functions import *
from .playerAbstract import PlayerAbstract

class Player(PlayerAbstract):
        def __init__(self, x, y):
            super().__init__(x, y)
            # Imagenes
            self.states = {
                "IDLE": Idle(False),
                "RUNR": Run(False, False),
                "RUNL": Run(False, True),
            }
            # Imagenes
            self.anim = 0 
            self.current_state = self.states["IDLE"]
            self.standing = self.current_state.get_initial()
            self.deadImage = pygame.transform.rotate(self.standing,90)
            self.hitImage = pygame.transform.rotate(self.standing,90)

        def move_left(self):
            self.moving_left = True

        def move_right(self):
            self.moving_right = True

        def jump(self):
            self.jumping = True

        def getHp(self):
            return self.healthPoints
        
        def hit(self):
            if self.hitCooldown < 0:
                self.standing = self.hitImage 
                self.healthPoints -= 1
                self.hitCooldown = 60
                self.notify()

        # La clase checkGunClollide deberia de eliminarse
        # Interact deberia de valer para todo objeto interactuable (Ordenador, puertas, luces, armas, vidas, mejoras...)
        # En world meter armas como un interactuable pygame.sprite.interacutableGroup
        def interact(self, interactuableGroup):
            interactsWith = pygame.sprite.spritecollideany(self, interactuableGroup)
            if interactsWith:
                newText = interactsWith.interact()
                if newText != self.interactuableText:
                    self.interactuableText = newText
                    self.notify()
            elif self.interactuableText != "":
                self.interactuableText = ""
                self.notify()
            
        def getInteractuableText(self):
            return self.interactuableText
                

        def update(self, world, dt, enemies_group, interactuableGroup, cameraOffset) -> tuple:

            cameraOffsetX, cameraOffsetY = cameraOffset

            self.interact(interactuableGroup)
            self.hitCooldown -= 1

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.velY = -10
            
            if self.anim > 6:
                self.standing = self.current_state.next_sprite()
                self.anim = 0
            self.anim += 1

            # Calculo del movimiento horizontal
            (self.left_mov, left_movement) = move_horizontal(self.moving_left, self.left_mov, dt)
            (self.right_mov, right_movement) = move_horizontal(self.moving_right, self.right_mov, dt)
            horizontal_movement = floor(right_movement - left_movement)

            # Calculo del movimiento vertical
            if self.jumping and self.inAir == False and self.pressed_jump == 0:
                self.velY = -MIN_JUMP_HEIGHT
                self.hold_jump = True
            elif self.jumping == False or self.pressed_jump > MAX_JUMP_HEIGHT:
                self.hold_jump = False
            elif self.jumping and self.inAir and self.hold_jump:
                self.velY = -MIN_JUMP_HEIGHT
                self.pressed_jump += 1

            # Para que al mantener el espacio solo salte una vez
            if self.jumping == False:
                self.pressed_jump = 0

            if horizontal_movement < 0:
                self.current_state = self.states["RUNL"]
            if horizontal_movement > 0:
                self.current_state = self.states["RUNR"]
            if horizontal_movement == 0: 
                self.current_state = self.states["IDLE"]

            # Se añade la gravedad al movimiento en y
            self.velY += GRAVITY
            if self.velY > MAX_FALL_VELOCITY:
                 self.velY = MAX_FALL_VELOCITY
            dy = self.velY
            dx = horizontal_movement

            self.inAir = True

            # Se calculan las colisiones en ambos ejes
            for tile in world.terrainHitBoxList:
                if tile.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                if tile.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.velY < 0: #Saltando
                        dy = tile.bottom - self.rect.top
                        self.velY = 0
                    elif self.velY >= 0: #Cayendo
                        dy = tile.top - self.rect.bottom
                        self.velY = 0
                        self.inAir = False
            
            cameraOffsetX = 0
            cameraOffsetY = 0

            # Si el jugador se mueve en los limites del scroll se mueve sin mas, si no se hace scroll
            if self.rect.x > SCREEN_WIDTH / 3 and self.rect.x < SCREEN_WIDTH - (SCREEN_WIDTH / 3):
                self.rect.x += dx 
            elif self.rect.x + dx > SCREEN_WIDTH / 3 and self.rect.x + dx < SCREEN_WIDTH - (SCREEN_WIDTH / 3):
                self.rect.x += dx 
            else:
                cameraOffsetX = dx

            if self.rect.y > (SCREEN_HEIGTH / 2) and self.rect.y < SCREEN_HEIGTH - (SCREEN_HEIGTH / 2):
                self.rect.y += dy
            elif self.rect.y + dy >= (SCREEN_HEIGTH / 2) and self.rect.y + dy <= SCREEN_HEIGTH - (SCREEN_HEIGTH / 2):
                self.rect.y += dy
            else:
                cameraOffsetY = dy

            # Se reinician las variables de movimiento
            self.moving_left = False
            self.moving_right = False
            self.jumping = False

            

            return (cameraOffsetX, cameraOffsetY)

        def checkGunPick(self, world):
            i = 0
            for gun in world.gun_list:
                if gun[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
                    del world.gun_list[i] # Se elimina la pistola de la lista de objetos
                    del gun # Se elimina el objeto pistola
                    return True # Devolver gun en vez de True para tener mas armas?
                i += 1
            
        def shoot(self, direction, gv):
            print("No tengo arma")

        def draw(self, screen):
            screen.blit(self.standing, self.rect)

        def addObserver(self, observer):
            self.uiElementsList.append(observer)
    
        def delObserver(self, observer):
            self.uiElementsList.remove(observer)

        def notify(self):
            for observer in self.uiElementsList:
                observer.update(self)

        def position(self):
            return self.rect