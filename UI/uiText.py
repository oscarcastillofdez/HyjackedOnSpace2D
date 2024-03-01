import pygame
from Constants.constants import *

class UIText():
    def __init__(self) -> None:
        self.font = pygame.font.Font(None, 96)
        self.surfaceText = None
        self.surfaceText = self.font.render("", True, "black")


    def setInteractualeText(self, text, color):
        self.surfaceText = self.font.render(text, True, color)

    def update(self, observable):
        self.setInteractualeText(observable.getInteractuableText(), "black")
        
    def draw(self, screen):
        screen.blit(self.surfaceText, (SCREEN_WIDTH / 2, SCREEN_HEIGTH / 2))
        
