import pygame

from Constants.constants import *
from Game.spritesheet import Spritesheet
from Constants.constants import *

class UIPistolUpgrade():
    def __init__(self) -> None:
        self.image = pygame.transform.scale(pygame.image.load(UI_PATH + 'upgrade_icon.png'),(64,64))

        
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 130
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