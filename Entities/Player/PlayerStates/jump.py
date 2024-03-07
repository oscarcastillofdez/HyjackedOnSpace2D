import pygame
from Game.spritesheet import Spritesheet
from .base import pState
from Constants.constants import *

class Jump(pState):
    def __init__(self, gun):
        super(Jump, self).__init__()
        self.spritesheet = Spritesheet(PLAYER_SPRITES_PATH + 'run-player.png',(96,96))
        
        self.posibleNexts = {
            "JUMP": "JUMP",
            "RUN_LEFT": "RUN",
            "RUN_RIGHT": "RUN",
            "IDLE": "IDLE",
            "SHOOT": "JUMP-SHOOT",
            "STOP-SHOOT": "JUMP"
        }

        self.gun = gun
        self.animation = self.spritesheet.get_animation(0,0,64,64,7,(255,0,0))
    
    def next_sprite(self):
        self.sprite_index += 1
        if self.sprite_index == len(self.animation):
            self.sprite_index = 0
        
        if self.left:
            sprite=pygame.transform.flip(self.animation[self.sprite_index], True, False)
        else:
            sprite = self.animation[self.sprite_index]

        sprite = pygame.transform.rotate(sprite,45*self.sprite_index)
        return sprite