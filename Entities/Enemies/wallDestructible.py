import pygame
from .entity import Entity
import math
from Constants.constants import *
from Entities.bullet import Bullet
from Animations.boxBreaking import BoxBreaking

class WallDestructible(pygame.sprite.Sprite, Entity):
    def __init__(self,x,y,hitBox) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(ENEMIES_PATH + 'Box.png'), (128, 128))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 128

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hitBox = hitBox

        self.boxBreaking = BoxBreaking()


    def update(self,cameraOffset):
        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]

    def destroy(self, back_animations, world):
        self.boxBreaking.rect.x = self.rect.centerx - 64
        self.boxBreaking.rect.y = self.rect.centery - 64
        self.boxBreaking.scale((128,128))
        self.boxBreaking.play()
        world.terrainHitBoxList.remove(self.hitBox)
        back_animations.add(self.boxBreaking)
        