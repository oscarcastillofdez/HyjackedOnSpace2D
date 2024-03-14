import pygame
from Constants.constants import *
from Entities.Player.playerWithShield import PlayerWithShield
from UI.uiEnergy import UIEnergy

class ShieldPickup(pygame.sprite.Sprite):
    def __init__(self,x,y) -> None:
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.transform.scale(pygame.image.load(PLAYER_PATH + "plasma_shield.png"), (64,64))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.name = 'shield'
    
    def update(self,cameraOffset):
        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]
    
    def collidesWithPlayer(self,player,gunsGroup):
        if self.rect.colliderect(player.position()):
            gunsGroup.remove(self)
            return True

    def getPlayerWithIt(self, player, ui, volume):
        newPlayer = PlayerWithShield(player, ui)
        newPlayer.setVolume(volume)
        #player.addObserver(ui.uiEnergy)
        #ui.uiEnergy.show()
        return newPlayer
