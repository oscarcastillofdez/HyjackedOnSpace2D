from .base import pState
from Constants.constants import *
from Game.spritesheet import Spritesheet

class Idle(pState):
    def __init__(self, gun):
        super(Idle, self).__init__()
        self.withoutgun = Spritesheet(PLAYER_SPRITES_PATH + 'idle-player.png',(100,100))
        self.animations = {
            "NOGUN": self.withoutgun.get_animation(0,0,64,64,7,(255,0,0)) 
        }
        #self.withgun = Spritesheet()
        if gun:
            #self.current_animation = ""
            pass
        else:
            self.animation = self.animations["NOGUN"]