import pygame
from Constants.constants import *
from Entities.Player.playerWithPistol import PlayerWithPistol
from Entities.Player.playerWithPistolUpgrade import PlayerWithPistolUpgrade

class PistolUpgrade(pygame.sprite.Sprite):
    def __init__(self,x,y) -> None:
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.transform.scale(pygame.image.load(PLAYER_PATH + "pistol_upgraded.png"), (64,45))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.name = 'pistolUpgrade'

    
    def update(self, cameraOffset):
        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]
    
    def collidesWithPlayer(self,player,gunsGroup):
        if self.rect.colliderect(player.position()):
            gunsGroup.remove(self)
            return True

    def getPlayerWithIt(self, player,ui, volume):
        newPlayer = PlayerWithPistolUpgrade(player, ui)
        newPlayer.setVolume(volume)
        newPlayer.changeStates()
        return newPlayer
