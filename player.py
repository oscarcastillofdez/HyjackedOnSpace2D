import pygame
from playerStates.idle import Idle
from playerStates.run import Run
from math import floor
from global_vars import *
from aux_functions import *
from playerAbstract import PlayerAbstract

class Player(PlayerAbstract):
        def __init__(self, x, y):
            super().__init__(x, y)

        def move_left(self):
            self.moving_left = True

        def move_right(self):
            self.moving_right = True

        def jump(self):
            self.jumping = True

        def getHp(self):
            return self.healthPoints
        
        def checkHit(self, enemies_group):
            if pygame.sprite.spritecollide(self, enemies_group, False):
                if self.hitCooldown < 0:
                    self.standing = self.hitImage 
                    self.healthPoints -= 1
                    self.hitCooldown = 60
                    
                    self.notify()
                    return True
                
        def update(self, world, globalVars, dt, enemies_group):
            self.hitCooldown -= 1
            
            if self.anim > 6:
                self.standing = self.current_state.next_sprite()
                self.anim = 0
            self.anim += 1

            # Calculo del movimiento horizontal
            (self.left_mov, left_movement) = move_horizontal(self.moving_left, self.left_mov, dt)
            (self.right_mov, right_movement) = move_horizontal(self.moving_right, self.right_mov, dt)
            horizontal_movement = floor(right_movement - left_movement)

            # Calculo del movimiento vertical
            if self.jumping and self.inAir == False:
                self.velY = -MIN_JUMP_HEIGHT
                self.hold_jump = True
                self.pressed_jump = 0
            elif self.jumping == False or self.pressed_jump > MAX_JUMP_HEIGHT:
                self.hold_jump = False
            elif self.jumping and self.inAir and self.hold_jump:
                self.velY = -MIN_JUMP_HEIGHT
                self.pressed_jump += 1

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
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.velY < 0: #Saltando
                        dy = tile[1].bottom - self.rect.top
                        self.velY = 0
                    elif self.velY >= 0: #Cayendo
                        dy = tile[1].top - self.rect.bottom
                        self.velY = 0
                        self.inAir = False
            
            globalVars.CAMERA_OFFSET_X = 0
            globalVars.CAMERA_OFFSET_Y = 0

            # Si el jugador se mueve en los limites del scroll se mueve sin mas, si no se hace scroll
            if self.rect.x > SCREEN_WIDTH / 3 and self.rect.x < SCREEN_WIDTH - (SCREEN_WIDTH / 3):
                self.rect.x += dx 
            elif self.rect.x + dx > SCREEN_WIDTH / 3 and self.rect.x + dx < SCREEN_WIDTH - (SCREEN_WIDTH / 3):
                self.rect.x += dx 
            else:
                globalVars.CAMERA_OFFSET_X = dx

            if self.rect.y > (SCREEN_HEIGTH / 2) and self.rect.y < SCREEN_HEIGTH - (SCREEN_HEIGTH / 2):
                self.rect.y += dy
            elif self.rect.y + dy >= (SCREEN_HEIGTH / 2) and self.rect.y + dy <= SCREEN_HEIGTH - (SCREEN_HEIGTH / 2):
                self.rect.y += dy
            else:
                globalVars.CAMERA_OFFSET_Y = dy

            self.checkHit(enemies_group)

            # Se reinician las variables de movimiento
            self.moving_left = False
            self.moving_right = False
            self.jumping = False


        def draw(self, screen):
            screen.blit(self.standing, self.rect)

        def addObserver(self, observer):
            self.uiElementsList.append(observer)
    
        def delObserver(self, observer):
            self.uiElementsList.remove(observer)

        def notify(self):
            for observer in self.uiElementsList:
                observer.update()