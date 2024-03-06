from .base import pState
from Constants.constants import *
from Game.spritesheet import Spritesheet

class IdleShooting(pState):
    def __init__(self):
        super(IdleShooting, self).__init__()
        self.animation = Spritesheet(PLAYER_SPRITES_PATH + 'idleShoot-player.png', (96,96)).get_animation(0,0,64,64,7,(255,0,0))

    