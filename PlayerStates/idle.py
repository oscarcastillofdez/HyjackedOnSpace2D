import pygame
from .base import pState
from spritesheet import Spritesheet

class Idle(pState):
    def __init__(self, gun):
        super(Idle, self).__init__()
        self.withoutgun = Spritesheet('Assets/player/idle-player.png',(100,100))
        self.animations = {
            "NOGUN": self.withoutgun.get_animation(0,0,64,64,7) 
        }
        #self.withgun = Spritesheet()
        if gun:
            #self.current_animation = ""
            pass
        else:
            self.current_animation = self.animations["NOGUN"]
    
    def get_initial(self):
        return self.withoutgun.get_sprite(0,0,64,64)
    
    def next_sprite(self):
        self.sprite_index += 1
        if self.sprite_index == len(self.current_animation):
            self.sprite_index = 0
        return self.current_animation[self.sprite_index]