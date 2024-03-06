import pygame
import math
from Constants.constants import *
from pyganim import PygAnimation
from Game.spritesheet import Spritesheet

class Animation(pygame.sprite.Sprite, PygAnimation):
    def __init__(self, *args):
        self.rect = pygame.Rect(0, 0, 10,10)
        self.rect.x = 0
        self.rect.y = 0

        PygAnimation.__init__(self, args[0], args[1])
        pygame.sprite.Sprite.__init__(self)
        

    def update(self, cameraOffset, back_animations):
        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]

        if self.isFinished():
            back_animations.remove(self)

    def draw(self, screen):
        self.blit(screen, (self.rect.x, self.rect.y))
