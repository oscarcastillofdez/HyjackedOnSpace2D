import pygame
from Constants.constants import *


class Trigger(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h,text):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("Assets/Images/Desorden/pruebasTrigger.png"),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = text
        self.active = False
        
    def interact(self):
        self.active = True
        

    def update(self, cameraOffset):
        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]
        if self.active:
            return self.text
        else:
            return ""
    
