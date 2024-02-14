import pygame
from global_vars import *

class Player():
        def __init__(self,x,y,screen,globalVars):
            self.screen = screen
            self.globalVars = globalVars
            self.reset(x,y)

        
        def update(self, GAME_OVER, world, enemies_group):

            # Si el juego esta en marcha
            if GAME_OVER == False:
                dx = 0
                dy = 0

                # Se detectan las teclas pulsadas
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    dx -= 7
                if keys[pygame.K_d]:
                    dx += 7
                if keys[pygame.K_SPACE] and self.jumped == False and self.inAir == False:
                    self.velY = -25
                    self.jumped = True
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
                        elif self.velY >= 0: #Callendo
                            dy = tile[1].top - self.rect.bottom
                            self.velY = 0
                            self.inAir = False

                    # Si toca un enemigo se acaba el juego
                    if pygame.sprite.spritecollide(self, enemies_group, False):
                        GAME_OVER = True
                        
                self.globalVars.CAMERA_OFFSET_X = 0

                # Si el jugador se mueve en los limites del scroll se mueve sin mas, si no se hace scroll
                if self.rect.x > SCREEN_WIDTH / 6 and self.rect.x < SCREEN_WIDTH - (SCREEN_WIDTH / 6):
                    self.rect.x += dx 
                elif self.rect.x + dx > SCREEN_WIDTH / 6 and self.rect.x + dx < SCREEN_WIDTH - (SCREEN_WIDTH / 6):
                    self.rect.x += dx 
                else:
                    self.globalVars.CAMERA_OFFSET_X = dx
                self.rect.y += dy

                # El borde inferior es un suelo
                if self.rect.bottom > SCREEN_HEIGTH:
                    self.rect.bottom = SCREEN_HEIGTH
                    self.inAir = False
                    dy = 0

            # Si se murio el jugador se cambia la imagen por la de muerte
            else:
                self.standing = self.deadImage
                

            self.screen.blit(self.standing, self.rect)
            return GAME_OVER

        def reset(self,x,y):
            self.standing = pygame.transform.scale(pygame.image.load("Assets/move1.png"), (100,100))
            self.rect = self.standing.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.width = self.standing.get_width()
            self.height = self.standing.get_height()
            self.velY = 0
            self.jumped = False
            self.inAir = True
            self.deadImage = pygame.transform.rotate(self.standing,90)