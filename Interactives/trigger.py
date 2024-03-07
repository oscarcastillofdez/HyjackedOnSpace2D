import pygame
from Constants.constants import *
import threading

class Trigger(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.rect(x,y,w,h)
        
    def interact(self):
        print("AAAAAAA")

    def update(self, cameraOffset, player):
        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]
