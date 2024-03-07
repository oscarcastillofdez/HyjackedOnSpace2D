from .base import pState
from Constants.constants import *
from Game.spritesheet import Spritesheet

class Idle(pState):
    def __init__(self, gun):
        super(Idle, self).__init__()
        self.left = True
        self.spritesheet = Spritesheet(PLAYER_SPRITES_PATH + 'idle-player.png',(100,100))

        self.posibleNexts = {
            "JUMP": "JUMP",
            "RUN_LEFT": "RUN",
            "RUN_RIGHT": "RUN",
            "IDLE": "IDLE",
            "SHOOT": "IDLE-SHOOT",
            "STOP-SHOOT": "IDLE"
        }

        if gun:
            self.animation = self.spritesheet.get_animation(0,0,64,64,6)
        else:
            self.animation = self.spritesheet.get_animation(0,0,64,64,6)