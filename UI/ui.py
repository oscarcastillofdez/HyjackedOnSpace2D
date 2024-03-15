import pygame
from Constants.constants import *

class Ui():
    def __init__(self, playerObservable, uiText, uiHearts, uiEnergy,uiCounter, bossHealthBar,rahmcroshair, uiPistol, uiPistolUpgrade, uiGrenadeLauncher, uiDash):
        self.playerObservable = playerObservable
        
        self.pickUpText = ""
        self.uiText = uiText
        self.uiHearts = uiHearts
        self.uiEnergy = uiEnergy
        self.uiCounter = uiCounter
        self.bossHealthBar = bossHealthBar
        self.rahmcroshair = rahmcroshair
        self.uiPistol = uiPistol
        self.uiPistolUpgrade = uiPistolUpgrade
        self.uiGrenadeLauncher = uiGrenadeLauncher
        self.uiDash = uiDash
    
    # def update(self):
        # self.hearts = pygame.transform.scale(pygame.image.load('Assets/img/hearts_'+ str(self.playerObservable.getHp()) +'.png').convert_alpha(), (180,100))
        # self.text.setInteractualeText(self.playerObservable.getInteractuableText(), "black")

    def draw(self, screen):
        self.uiHearts.draw(screen)
        self.uiText.draw(screen)
        self.uiEnergy.draw(screen)
        self.uiCounter.draw(screen)
        self.bossHealthBar.draw(screen)
        self.rahmcroshair.draw(screen)
        self.uiPistol.draw(screen)
        self.uiPistolUpgrade.draw(screen)
        self.uiGrenadeLauncher.draw(screen)
        self.uiDash.draw(screen)
