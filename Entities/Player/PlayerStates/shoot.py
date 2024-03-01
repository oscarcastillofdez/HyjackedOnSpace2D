from .base import pState
from Game.spritesheet import Spritesheet
from Constants.constants import *

class Shoot(pState):
    def __init__(self, direction):
        super(Shoot, self).__init__()
        self.animation = None
        if direction == 0:
            self.animation = Spritesheet(PLAYER_SPRITES_PATH + "RunShootLeft.png", (100,100)).get_animation(0,0,64,64,4)
        if direction == 180:
            self.animation = Spritesheet(PLAYER_SPRITES_PATH + "RunShootRight.png", (100,100)).get_animation(0,0,64,64,4)
        """if direction == "downR":
            self.animation = Spritesheet("Assets/player/RunShootDownR").get_animation()
        if direction == "up":
            self.animation = Spritesheet("Assets/player/RunShootDownL").get_animation()"""
        
    def initial(self):
        return self.animation[0]
