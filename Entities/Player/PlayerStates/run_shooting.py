from .base import pState
from Constants.constants import *
from Game.spritesheet import Spritesheet

class RunShootingRight(pState):
    def __init__(self):
        super(RunShootingRight, self).__init__()
        self.animation = Spritesheet(PLAYER_SPRITES_PATH + 'RunShootRight-player.png', (96,96))
    
class RunShootingLeft(pState):
    def __init__(self):
        super(RunShootingLeft, self).__init__()
        self.animation = Spritesheet(PLAYER_SPRITES_PATH + "RunShootLeft-player.png",(96,96))
