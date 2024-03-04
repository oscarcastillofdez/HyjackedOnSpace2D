import pygame
from Game.spritesheet import Spritesheet
from .base import pState
from Constants.constants import *

class Jump(pState):
    def __init__(self, gun):
        super(Jump, self).__init__()
        self.spritesheet = Spritesheet(PLAYER_SPRITES_PATH + 'run-player.png',(96,96))
        
        self.gun = gun
        self.animation = self.spritesheet.get_animation(0,0,64,64,7)
        self.current = self.animation[0]
        self.count = 1
    
    
    def next_sprite(self):
        self.sprite_index += 1
        if self.sprite_index == len(self.animation):
            self.sprite_index = 0

        res = pygame.transform.rotate(self.animation[self.sprite_index],45*self.sprite_index)
        return res