import pygame
from Constants.constants import *

# Seria mas inteligente en vez de pasarle en el constructor todos los elementos de la interfaz
# En vez de eso, hacer una lista uiElementsList e ir agregando y quitando ahi elementos segun se vayan a ver o no
# Asi no tendriamos que estar en cada uno con toggleShow para ocultarlos
class Ui():
    def __init__(self, uiText, uiHearts, uiEnergy,uiCounter, bossHealthBar,rahmcroshair, uiPistol, uiPistolUpgrade, uiGrenadeLauncher, uiDash):
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
        #self.uiElementsList = []
    
    #def addUiElement(self, uiElement):
        #self.uiElementsList.append(uiElement)

    def draw(self, screen):
        #for uiElement in self.uiElementsList:
            #uiElement.draw(screen)

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
