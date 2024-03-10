import pygame
from Game.spritesheet import Spritesheet
from .base import pState
from Constants.constants import *

class Jump(pState):
    def __init__(self, gun):
        super(Jump, self).__init__()
    
        self.posibleNexts = {
            "JUMP": "JUMP",
            "RUN": "RUN",
            "IDLE": "IDLE",
            "SHOOT": "JUMP-SHOOT",
            "STOP-SHOOT": "JUMP",
            "STOP-JUMP": "IDLE"
        }

        """
            "SHOOT": "JUMP-SHOOT",
            "SHOOT-DOWN": "JUMP-SHOOT",
            "SHOOT-UP": "JUMP-SHOOT",
            "SHOOT-DIAG-DOWN":"JUMP-SHOOT",
            "SHOOT-DIAG-UP": "JUMP-SHOOT",
        """
        if gun:
            self.animation = Spritesheet(PLAYER_SPRITES_PATH + 'JumpGun-player.png',(96,96)).get_sprite(0,0,64,64,(255,0,0))
        else:
            self.animation = Spritesheet(PLAYER_SPRITES_PATH + 'Jump-player.png',(96,96)).get_sprite(0,0,64,64,(255,0,0))
    
    def next_sprite(self, direction):
        if self.left:
            sprite=pygame.transform.flip(self.animation, True, False)
        else:
            sprite = self.animation
        return sprite

class JumpShoot(pState):
    def __init__(self):
        super(JumpShoot, self).__init__()
        self.animation = Spritesheet(PLAYER_SPRITES_PATH + 'JumpNoArm-player.png', (96,96)).get_sprite(0,0,64,64,(255,0,0))
        
        self.DiagDownArm = Spritesheet(PLAYER_SPRITES_PATH + 'DiagDownArms-player.png', (96,96)).get_sprite(0,0,64,64,(255,0,0))
        self.DiagUpArm =   Spritesheet(PLAYER_SPRITES_PATH + 'UpArms-player.png', (96,96)).get_sprite(0,0,64,64,(255,0,0))
        self.UpArm =   Spritesheet(PLAYER_SPRITES_PATH + 'DownArms-player.png', (96,96)).get_sprite(0,0,64,64,(255,0,0))
        self.DownArm =   Spritesheet(PLAYER_SPRITES_PATH + 'DiagArms-player.png', (96,96)).get_sprite(0,0,64,64,(255,0,0))
        self.arm = Spritesheet(PLAYER_SPRITES_PATH + 'Arm-player.png', (96,96)).get_sprite(0,0,64,64,(255,0,0))
        
        self.posibleNexts = {
            "JUMP": "JUMP-SHOOT",
            "RUN": "RUN-SHOOT",
            "IDLE": "IDLE",
            "SHOOT": "JUMP-SHOOT",
            "STOP-SHOOT": "JUMP",
            "STOP-JUMP": "IDLE-SHOOT"
        }
        """
            "SHOOT-DOWN": "JUMP-SHOOT",
            "SHOOT-UP": "JUMP-SHOOT",
            "SHOOT-DIAG-DOWN":"JUMP-SHOOT",
            "SHOOT-DIAG-UP": "JUMP-SHOOT",
        """
    
    def next_sprite(self, direction):
        sprite = self.animation

        if direction:
            if direction == 0 or direction == 180:
                arms = self.arm
            if direction == 45 or direction == 315:
                arms = self.DiagUpArm
            if direction == 90:
                arms = self.UpArm
            if direction == 135 or direction == 315:
                arms = self.DiagDownArm
            if direction == 270:
                arms = self.DownArm
        
            sprite.blit(arms,(0,0),(0,0,96,96))

        #arms = arms[self.arm_index]
        if self.left:
            sprite=pygame.transform.flip(self.animation, True, False)

        return sprite
