import pygame
from Constants.constants import *

class UIBossHealthBar():
    def __init__(self) -> None:
        self.currentHealth = 1
        self.healthBarLength = SCREEN_WIDTH - 100
        self.maxHP = 1
        self.healthRatio = self.maxHP / self.healthBarLength

        self.posX = 40
        self.posY = SCREEN_HEIGTH - 50

        self.healthBarRect = pygame.Rect(self.posX,self.posY,self.currentHealth / self.healthRatio,25)
        self.transitionBarRect = pygame.Rect(self.posX,self.posY,self.currentHealth / self.healthRatio,25)

        self.transitionWidth = self.healthBarRect.width
        self.transitionColor = (255,0,0)

        self.show = False

    
    def update(self, observable):
        self.currentHealth = observable.getHp()
        self.targetHealth = observable.getTargetHealth()

    def setMaxHp(self, hp):
        self.maxHP = hp
        self.currentHealth = self.maxHP
        self.healthRatio = self.maxHP / self.healthBarLength

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
            
    def getHealth(self):
        return self.currentHealth