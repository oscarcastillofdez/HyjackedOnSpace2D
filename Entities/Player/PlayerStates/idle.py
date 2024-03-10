from .base import pState
from Constants.constants import *
from Game.spritesheet import Spritesheet
import pygame

class Idle(pState):
    def __init__(self, gun):
        super(Idle, self).__init__()
        self.left = True
        self.posibleNexts = {
            "JUMP": "JUMP",
            "RUN": "RUN",
            "IDLE": "IDLE",
            "SHOOT": "IDLE-SHOOT",
            "STOP-SHOOT": "IDLE"
        }
        """
            "SHOOT-DOWN": "IDLE-SHOOT-DIAG-DOWN",
            "SHOOT-UP": "IDLE-SHOOT-UP",
            "SHOOT-DIAG-DOWN":"IDLE-SHOOT-DIAG-DOWN",
            "SHOOT-DIAG-UP": "IDLE-SHOOT-DIAG-UP",
        """

        if gun:
            self.animation = Spritesheet(PLAYER_SPRITES_PATH + 'IdleGun-player.png',(96,96)).get_animation(0,0,64,64,8,(255,0,0))
        else:
            self.animation = Spritesheet(PLAYER_SPRITES_PATH + 'Idle-player.png',(96,96)).get_animation(0,0,64,64,8,(255,0,0))
    
class IdleShoot(pState):
    def __init__(self):
        super(IdleShoot, self).__init__()
        self.animation = Spritesheet(PLAYER_SPRITES_PATH + 'IdleNoArm-player.png', (96,96)).get_animation(0,0,64,64,8,(255,0,0))
        self.DiagDownArm = Spritesheet(PLAYER_SPRITES_PATH + 'DiagDownArms-player.png', (96,96)).get_sprite(0,0,64,64,(255,0,0))
        self.DiagUpArm =   Spritesheet(PLAYER_SPRITES_PATH + 'UpArms-player.png', (96,96)).get_sprite(0,0,64,64,(255,0,0))
        self.UpArm =   Spritesheet(PLAYER_SPRITES_PATH + 'DownArms-player.png', (96,96)).get_sprite(0,0,64,64,(255,0,0))
        self.DownArm =   Spritesheet(PLAYER_SPRITES_PATH + 'DiagArms-player.png', (96,96)).get_sprite(0,0,64,64,(255,0,0))
        self.arm = Spritesheet(PLAYER_SPRITES_PATH + 'Arm-player.png', (96,96)).get_sprite(0,0,64,64,(255,0,0))

        self.posibleNexts = {
            "JUMP": "JUMP-SHOOT",
            "RUN": "RUN-SHOOT",
            "IDLE": "IDLE",
            "SHOOT": "IDLE-SHOOT",
            "STOP-SHOOT": "IDLE",
        }
        """
            "SHOOT-DOWN": "IDLE-SHOOT-DIAG-DOWN",
            "SHOOT-UP": "IDLE-SHOOT-UP",
            "SHOOT-DIAG-DOWN":"IDLE-SHOOT-DIAG-DOWN",
            "SHOOT-DIAG-UP": "IDLE-SHOOT-DIAG-UP",
        """
    
    def next_sprite(self, direction):
        self.sprite_index += 1
        if self.sprite_index == len(self.animation):
            self.sprite_index = 0
        
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
        
        """if self.arm_index == len(arms):
            self.arm_index = 0"""
        sprite = self.animation[self.sprite_index]
        sprite.blit(arms,(0,0),(0,0,96,96))

        #arms = arms[self.arm_index]
        if self.left:
            sprite=pygame.transform.flip(sprite, True, False)

        return sprite