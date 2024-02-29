import pygame
from Game.spritesheet import Spritesheet
from .base import pState

class Jump(pState):
    def __init__(self):
        super(Jump, self).__init__()
        self.spritesheet = Spritesheet('Assets/player/jump-player.png',(100,100))
        
        self.animation = self.spritesheet.get_animation(0,0,64,64,7)
        self.current = self.animation[0]
    
    def initial(self):
        return self.spritesheet.get_sprite(0,0,64,64)
    
    def next_sprite(self):
        self.sprite_index += 1
        if self.sprite_index == len(self.animation):
            self.sprite_index = 0
        """
        self.current = self.animation[self.sprite_index]
        """
        res = pygame.transform.rotate(self.animation[self.sprite_index],45*self.sprite_index)
        return res