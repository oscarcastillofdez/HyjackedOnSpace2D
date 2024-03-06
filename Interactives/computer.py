import pygame
from Constants.constants import *
class Computer(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(INTERACTIVES_PATH + 'ibm5150.png'),(64,64))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def interact(self):
        return "Presiona E para interactuar."

    def update(self, player, cameraOffset):
        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]
