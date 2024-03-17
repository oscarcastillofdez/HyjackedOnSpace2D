import pygame
from Constants.constants import *

class UIText():
    def __init__(self) -> None:
        self.font = pygame.font.Font(None, 40)
        self.surfaceText = None
        self.surfaceText = self.font.render("", True, (255,255,255))


    def setInteractualeText(self, text, color):
        self.surfaceText = self.font.render(text, True, color)

    def update(self, observable):
        self.setInteractualeText(observable.getInteractuableText(), (255,255,255))
        
    def draw(self, screen):
        screen.blit(self.surfaceText, (SCREEN_WIDTH / 2, SCREEN_HEIGTH / 2))
        
