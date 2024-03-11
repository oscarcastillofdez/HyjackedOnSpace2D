import pygame
from Constants.constants import *

class UIVonregHealthBar():
    def __init__(self) -> None:
        self.currentHealth = 0
        self.healthBarLength = SCREEN_WIDTH - 100
        self.healthRatio = 300 / self.healthBarLength

        

        self.posX = 40
        self.posY = SCREEN_HEIGTH - 50

        self.healthBarRect = pygame.Rect(self.posX,self.posY,self.currentHealth / self.healthRatio,25)
        self.transitionBarRect = pygame.Rect(self.posX,self.posY,self.currentHealth / self.healthRatio,25)

        self.transitionWidth = self.healthBarRect.width
        self.transitionColor = (255,0,0)

        self.show = True

    
    def update(self, observable):
        self.currentHealth = observable.getHp()
        self.targetHealth = observable.getTargetHealth()

    def draw(self, screen):
        if self.show:
            pygame.draw.rect(screen, (255,0,0), (self.posX,self.posY,self.currentHealth / self.healthRatio,25))
            pygame.draw.rect(screen, (255,255,255), (self.posX,self.posY,self.healthBarLength,25), 4)
        else:
            pygame.draw.rect(screen, (255,0,0), (self.posX,self.posY,0,25))
            pygame.draw.rect(screen, (255,255,255), (self.posX,self.posY,0,25), 4)

    def togleShow(self):
        if self.show:
            self.show = False
        else:
            self.show = True
            