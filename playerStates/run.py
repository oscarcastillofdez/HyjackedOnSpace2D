import pygame
from spritesheet import Spritesheet
from .base import pState

class Run(pState):
    def __init__(self, gun, left):
        super(Run, self).__init__()
        self.left = left
        self.gun = gun
        if gun:
            if left:
                # Spritesheet runLeftGun-player
                self.spritesheet = Spritesheet('Assets/player/runLeftGun-player.png',(100,100))
            else:
                # Spritesheet runGun-player
                self.spritesheet = Spritesheet('Assets/player/runGun-player.png',(100,100))
                pass
        else:
            if left:
                # Spritesheet runLeft-player
                self.spritesheet = Spritesheet('Assets/player/runLeft-player.png',(100,100))
                pass
            else:
                #Spritesheet run-player
                self.spritesheet = Spritesheet('Assets/player/run-player.png',(100,100))
        self.animation = self.spritesheet.get_animation(0,0,64,64,6)
    
    def initial(self):
        return self.spritesheet.get_sprite(0,0,64,64)
    
    def next_sprite(self):
        self.sprite_index += 1
        if self.sprite_index == len(self.animation):
            self.sprite_index = 0
        return self.animation[self.sprite_index]