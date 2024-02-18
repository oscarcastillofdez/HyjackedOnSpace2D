import pygame
from playerStates.idle import Idle
from playerStates.run import Run
from global_vars import *

class Player():
        def __init__(self,x,y):
            # Imagenes
            self.states = {
                "IDLE": Idle(False),
                "RUNR": Run(False, False),
                "RUNL": Run(False, True),
                "RUNGL": Run(gun=True,left=True),
                "RUNGR": Run(gun=True, left=False)
            }
            self.current_state = self.states["IDLE"]
            self.anim = 0
            self.standing = self.current_state.get_initial()
            self.deadImage = pygame.transform.rotate(self.standing,90)

            # Posicion
            self.rect = self.standing.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.width = self.standing.get_width()
            self.height = self.standing.get_height()
            self.velY = 0
            self.jumped = False
            self.inAir = True

        def get_event(self, event):
            pass

        def update(self, world, globalVars):
            if self.anim > 6:
                self.standing = self.current_state.next_sprite()
                self.anim = 0
            self.anim += 1
            dx = 0
            dy = 0

            # Se detectan las teclas pulsadas
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.current_state = self.states["RUNL"]
                dx -= 7
            if keys[pygame.K_d]:
                self.current_state = self.states["RUNR"]
                dx += 7
            if keys[pygame.K_SPACE] and self.jumped == False and self.inAir == False:
                self.velY = -25
                self.jumped = True
            if keys[pygame.K_s]:
                self.current_state = self.states["IDLE"]
            if keys[pygame.K_SPACE] == False:
                self.jumped = False
            # Se añade la gravedad al movimiento en y
            self.velY += 1
            if self.velY > 10:
                 self.velY = 10
            dy += self.velY

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
                    
            #print(self.rect.bottom)
            # El borde inferior es un suelo
            if self.rect.bottom > SCREEN_HEIGTH:
                self.rect.bottom = SCREEN_HEIGTH
                self.inAir = False
                dy = 0
        
        def draw(self, screen):
            screen.blit(self.standing, self.rect)
