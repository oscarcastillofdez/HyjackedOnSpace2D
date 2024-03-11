import pygame
from Constants.constants import *

class Ui():
    def __init__(self, playerObservable, uiText, uiHearts, uiEnergy,uiCounter, uiVonregHealthBar):
        self.playerObservable = playerObservable
        
        self.pickUpText = ""
        self.uiText = uiText
        self.uiHearts = uiHearts
        self.uiEnergy = uiEnergy
        self.uiCounter = uiCounter
        self.uiVonregHealthBar = uiVonregHealthBar
    
    # def update(self):
        # self.hearts = pygame.transform.scale(pygame.image.load('Assets/img/hearts_'+ str(self.playerObservable.getHp()) +'.png').convert_alpha(), (180,100))
        # self.text.setInteractualeText(self.playerObservable.getInteractuableText(), "black")

    def draw(self, screen):
        self.uiHearts.draw(screen)
        self.uiText.draw(screen)
        self.uiEnergy.draw(screen)
        self.uiCounter.draw(screen)
        self.uiVonregHealthBar.draw(screen)
