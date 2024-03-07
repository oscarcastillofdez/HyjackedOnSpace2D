import pygame
from Constants.constants import *

class UICounter():
    def __init__(self) -> None:
        self.font = pygame.font.Font(None, 96)
        self.surfaceText = None
        self.surfaceText = self.font.render("", True, (255,255,255))

        self.posX = SCREEN_WIDTH / 2
        self.posY = 30

    def setInteractualeText(self, text, color):
        self.surfaceText = self.font.render(text, True, color)

    def update(self, observable):
        counter = observable.getCounter()
        if counter == "0":
            counter = ""
        self.setInteractualeText(counter, "black")
        
    def draw(self, screen):
        screen.blit(self.surfaceText, (self.posX, self.posY))
        
