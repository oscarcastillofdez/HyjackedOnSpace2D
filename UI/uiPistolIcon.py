import pygame

from Constants.constants import *
from Game.spritesheet import Spritesheet
from Constants.constants import *

class UIPistol():
    def __init__(self) -> None:
        self.image = pygame.transform.scale(pygame.image.load(UI_PATH + 'pistol.png'), (52,41.5))

        
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = 175
        self.show = False

    def update(self, player):
        # cooldown = player.getCooldown()
        pass
    
    def draw(self,screen):
        if self.show:
            screen.blit(self.image, self.rect)

    def uIShow(self):
        self.show = True
    def uIHide(self):
        self.show = False