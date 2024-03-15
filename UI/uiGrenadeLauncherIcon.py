import pygame

from Constants.constants import *
from Game.spritesheet import Spritesheet
from Constants.constants import *

class UIGrenadeLauncher():
    def __init__(self) -> None:
        self.image = pygame.transform.scale2x(pygame.image.load(UI_PATH + 'grenade_launcher_grey.png'))

        
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = 250
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