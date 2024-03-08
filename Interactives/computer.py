import time
import pygame
from Constants.constants import *
from Entities.Enemies.randomEnemyFactorySecuence import RandomEnemyFactorySecuence
from UI.uiCounter import UICounter
import threading

class Computer(pygame.sprite.Sprite):
    def __init__(self,x,y,enemy_factory):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(INTERACTIVES_PATH + 'ibm5150.png'),(64,64))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #self.interactiveIndicator = InteractiveIndicator(x, y)

        self.randomEnemyFactorySecuence = enemy_factory
        
    def interact(self):
        self.randomEnemyFactorySecuence.activate()

    def update(self, cameraOffset):
        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]

        self.randomEnemyFactorySecuence.update(self.rect.x, self.rect.y)
            

    def getText(self):
        return "Presiona E para interactuar."
    
    
        