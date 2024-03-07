from Game.spritesheet import Spritesheet
from .base import pState
from Constants.constants import *
import pygame

class Run(pState):
    def __init__(self, gun):
        super(Run, self).__init__()
        self.gun = gun
        
        self.posibleNexts = {
            "JUMP": "JUMP",
            "RUN_LEFT": "RUN",
            "RUN_RIGHT": "RUN",
            "IDLE": "IDLE",
            "SHOOT": "RUN-SHOOT",
            "STOP-SHOOT": "RUN"
        }

        if gun:
            self.spritesheet = Spritesheet(PLAYER_SPRITES_PATH + 'RunGunRight-player.png',(100,100))
        else:
            #Spritesheet run-player
            self.spritesheet = Spritesheet(PLAYER_SPRITES_PATH + 'RunRight-player.png',(100,100))
        self.animation = self.spritesheet.get_animation(0,0,64,64,6,(255,0,0))