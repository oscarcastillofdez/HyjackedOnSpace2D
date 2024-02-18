import pygame
from math import floor
from global_vars import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,globalVars):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('Assets/img/pj.png'), (120, 120))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 100
        self.move_dir = 1
        self.moved = 0
        self.globalVars = globalVars
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.inAir = True
        self.velY = 0

    # Se mueve el enemigo en una dirección hasta que llega al limite donde se cambia.
    def update(self, world):
        dy = 0

        self.inAir = True
        self.moved += 1
        if self.moved >= 400:
            self.move_dir = -self.move_dir
            self.moved = 0

        self.velY += 1
        if self.velY > 10:
             self.velY = 10
        dy += self.velY
        
        # Se calculan las colisiones en ambos ejes
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + self.move_dir, self.rect.y, self.width, self.height):
                self.move_dir = -self.move_dir
            
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.velY < 0: #Saltando
                        dy = tile[1].bottom - self.rect.top
                        print(dy)
                        self.velY = 0
                    elif self.velY >= 0: #Cayendo
                        dy = tile[1].top - self.rect.bottom
                        self.velY = 0
                        self.inAir = False
                        
        self.rect.x += self.move_dir - self.globalVars.CAMERA_OFFSET_X
        self.rect.y += dy - self.globalVars.CAMERA_OFFSET_Y
        #pygame.draw.rect(screen, (255,255,255), self.rect)
