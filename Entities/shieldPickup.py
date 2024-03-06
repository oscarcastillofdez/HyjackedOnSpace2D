import pygame
from Constants.constants import *
from Entities.Player.playerWithShield import PlayerWithShield
from UI.uiEnergy import UIEnergy

class ShieldPickup(pygame.sprite.Sprite):
    def __init__(self,x,y) -> None:
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(PLAYER_PATH + "plasma_shield.png")

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self,cameraOffset):
        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]
    
    def collidesWithPlayer(self,player,gunsGroup):
        if self.rect.colliderect(player.position()):
            gunsGroup.remove(self)
            return True

    def getPlayerWithIt(self, player, ui):
        #player.addObserver(ui.uiEnergy)
        #ui.uiEnergy.show()
        return PlayerWithShield(player, ui)
