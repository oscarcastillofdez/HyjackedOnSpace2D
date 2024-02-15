import pygame
from math import floor
from global_vars import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,globalVars):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('Assets/img/pj.png'), (120, 120))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_dir = 1
        self.moved = 0
        self.globalVars = globalVars

    # Se mueve el enemigo en una dirección hasta que llega al limite donde se cambia.
    def update(self):

        print("CCCCCCCCCCCCCc")
        self.moved += 1
        if self.moved == 50:
            self.move_dir = -self.move_dir
            self.moved = 0

        self.rect.x += self.move_dir - self.globalVars.CAMERA_OFFSET_X
        self.rect.y -= self.globalVars.CAMERA_OFFSET_Y
