import pygame
from Constants.constants import *
from Entities.Player.playerWithDash import PlayerWithDash

class Dash(pygame.sprite.Sprite):
    def __init__(self,x,y) -> None:
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.transform.scale2x(pygame.image.load(INTERACTIVES_PATH + "CinturonCobete.png"))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.name = 'dash'

    
    def update(self,cameraOffset):
        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]
    
    def collidesWithPlayer(self,player,gunsGroup):
        if self.rect.colliderect(player.position()):
            gunsGroup.remove(self)
            return True

    def getPlayerWithIt(self, player, ui, volume):
        newPlayer = PlayerWithDash(player,ui)
        newPlayer.setVolume(volume)
        return newPlayer
