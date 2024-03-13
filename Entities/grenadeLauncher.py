import pygame
from Constants.constants import *
from Entities.Player.playerWithGrenadeLauncher import PlayerWithGrenadeLauncher

class GrenadeLauncher(pygame.sprite.Sprite):
    def __init__(self,x,y) -> None:
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.transform.scale2x(pygame.image.load(INTERACTIVES_PATH + "grenade_launcher_grey.png"))

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
        newPlayer = PlayerWithGrenadeLauncher(player,ui)
        #newPlayer.changeStates()
        return newPlayer
