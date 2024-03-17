import pygame
import math
from Constants.constants import *
from Entities.bullet import Bullet
from Animations.boxBreaking import BoxBreaking

class WallDestructible(pygame.sprite.Sprite):
    def __init__(self,x,y,destructibleTile_list) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(ENEMIES_PATH + 'Box.png'), (128, 128))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.boxBreaking = BoxBreaking()
        self.destructibleTile_list = destructibleTile_list


    def update(self,cameraOffset):
        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]

    def destroy(self, back_animations, world, destructibles_group):
        self.boxBreaking.rect.x = self.rect.centerx - 64
        self.boxBreaking.rect.y = self.rect.centery - 64
        self.boxBreaking.scale((128,128))
        self.boxBreaking.play()
        self.destructibleTile_list.remove(self.rect)
        destructibles_group.remove(self)
        back_animations.add(self.boxBreaking)
    
    def draw(self,screen):
        pass
        #pygame.draw.rect(screen, (255,255,255), self.rect)