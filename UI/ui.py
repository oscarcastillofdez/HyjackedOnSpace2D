import pygame
from global_varsClass import Global_Vars

class Ui():
    def __init__(self, playerObservable, uiText, uiHearts):
        self.playerObservable = playerObservable
        
        self.pickUpText = ""
        self.gv = Global_Vars()
        self.uiText = uiText
        self.uiHearts = uiHearts
    
    # def update(self):
        # self.hearts = pygame.transform.scale(pygame.image.load('Assets/img/hearts_'+ str(self.playerObservable.getHp()) +'.png').convert_alpha(), (180,100))
        # self.text.setInteractualeText(self.playerObservable.getInteractuableText(), "black")

    def draw(self, screen):
        
        self.uiHearts.draw(screen)
        self.uiText.draw(screen)
