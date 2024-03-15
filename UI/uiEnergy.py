import pygame

from Constants.constants import *
from Game.spritesheet import Spritesheet
from Constants.constants import *

class UIEnergy():
    def __init__(self) -> None:
        self.spritesheet = Spritesheet(UI_PATH + 'shield_energy.png', (100,100))
        
        # Cargar sprites
        self.spriteList = self.spritesheet.cargar_sprites(64, 96)
        self.currentEnergy = self.spriteList[13]

        self.rect = self.currentEnergy.get_rect()
        self.rect.x = SCREEN_WIDTH - (120)
        self.rect.y = 30
        self.hide = True

    def update(self, player):
        vida = player.getShieldHp()
        self.currentEnergy = self.spriteList[11-vida]
    
    def draw(self,screen):
        if self.hide == False:
            screen.blit(self.currentEnergy, self.rect)

    def show(self):
        self.hide = False
        self.currentEnergy = self.spriteList[0]

    def hide(self):
        self.hide = True