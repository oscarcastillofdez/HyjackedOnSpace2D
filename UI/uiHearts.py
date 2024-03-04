import pygame
from Constants.constants import *

class UIHearts():
    def __init__(self) -> None:
        self.hearts3 = pygame.transform.scale(pygame.image.load(UI_PATH + 'hearts_3.png').convert_alpha(), (180,100))
        self.hearts2 = pygame.transform.scale(pygame.image.load(UI_PATH + 'hearts_2.png').convert_alpha(), (180,100))
        self.hearts1 = pygame.transform.scale(pygame.image.load(UI_PATH + 'hearts_1.png').convert_alpha(), (180,100))
        self.hearts0 = pygame.transform.scale(pygame.image.load(UI_PATH + 'hearts_0.png').convert_alpha(), (180,100))
        
        self.heartsList = [self.hearts0, self.hearts1, self.hearts2, self.hearts3]
        self.hearts = self.heartsList[3]

        self.rect = self.hearts.get_rect()
        self.rect.x = 30
        self.rect.y = 30
    
    def update(self, observable):
        self.hearts = self.heartsList[observable.getHp()]
    
    def draw(self, screen):
        screen.blit(self.hearts, self.rect)
