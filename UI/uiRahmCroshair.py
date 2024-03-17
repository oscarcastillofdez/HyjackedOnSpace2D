import pygame

from Constants.constants import *

from Constants.constants import *

class UIRahmCroshair():
    def __init__(self) -> None:
        self.image = pygame.transform.scale(pygame.image.load(UI_PATH + 'croshair_rahm.png'),(128,115))
        
        # Cargar sprites

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.show = False

    def update(self, observable):
        playerPos = observable.getPlayerPosition()

        self.rect.centerx = playerPos.centerx
        self.rect.centery = playerPos.centery
    
    def draw(self,screen):
        if self.show:
            screen.blit(self.image, self.rect)

    def togleShow(self, value):
        self.show = value
  