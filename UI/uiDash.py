import pygame

from Constants.constants import *
from Game.spritesheet import Spritesheet
from Constants.constants import *

class UIDash():
    def __init__(self) -> None:
        self.image = pygame.transform.scale2x(pygame.image.load(INTERACTIVES_PATH + "CinturonCobete.png"))

        
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = 300
        self.show = False

    def update(self, player):
        # cooldown = player.getCooldown()
        pass
    
    def draw(self,screen):
        if self.show:
            screen.blit(self.image, self.rect)

    def toggleShow(self):
        if self.show:
            self.show = False
        else:
            self.show = True