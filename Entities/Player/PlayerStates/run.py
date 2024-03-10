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
            "RUN": "RUN",
            "IDLE": "IDLE",
            "SHOOT": "RUN-SHOOT",
            "STOP-SHOOT": "RUN",
            "STOP-JUMP": "RUN"
        }

        """
            "SHOOT-DOWN": "RUN-SHOOT-DOWN",
            "SHOOT-UP": "RUN-SHOOT-UP",
            "SHOOT-DIAG-DOWN":"RUN-SHOOT-DIAG-DOWN",
            "SHOOT-DIAG-UP": "RUN-SHOOT-DIAG-UP",
        """

        if gun:
            self.spritesheet = Spritesheet(PLAYER_SPRITES_PATH + 'RunGun-player.png',(96,96))
        else:
            #Spritesheet run-player
            self.spritesheet = Spritesheet(PLAYER_SPRITES_PATH + 'Run-player.png',(96,96))
        self.animation = self.spritesheet.get_animation(0,0,64,64,6,(255,0,0))

class RunShoot(pState):
    def __init__(self):
        super(RunShoot, self).__init__()
        self.animation = Spritesheet(PLAYER_SPRITES_PATH + 'NoArmsRun-player.png', (96,96)).get_animation(0,0,64,64,6,(255,0,0))
        
        self.DiagDownArm = Spritesheet(PLAYER_SPRITES_PATH + 'DiagDownArms-player.png', (96,96)).get_sprite(0,0,64,64,(255,0,0))
        self.DiagUpArm =   Spritesheet(PLAYER_SPRITES_PATH + 'UpArms-player.png', (96,96)).get_sprite(0,0,64,64,(255,0,0))
        self.UpArm =   Spritesheet(PLAYER_SPRITES_PATH + 'DownArms-player.png', (96,96)).get_sprite(0,0,64,64,(255,0,0))
        self.DownArm =   Spritesheet(PLAYER_SPRITES_PATH + 'DiagArms-player.png', (96,96)).get_sprite(0,0,64,64,(255,0,0))
        self.arm = Spritesheet(PLAYER_SPRITES_PATH + 'Arm-player.png', (96,96)).get_sprite(0,0,64,64,(255,0,0))
        
        self.posibleNexts = {
            "JUMP": "JUMP-SHOOT",
            "RUN": "RUN-SHOOT",
            "IDLE": "IDLE-SHOOT",
            "SHOOT": "RUN-SHOOT",
            "STOP-SHOOT": "RUN",
            "STOP-JUMP": "RUN-SHOOT"
        }
        """
            "SHOOT-DOWN": "RUN-SHOOT-DOWN",
            "SHOOT-UP": "RUN-SHOOT-UP",
            "SHOOT-DIAG-DOWN":"RUN-SHOOT-DIAG-DOWN",
            "SHOOT-DIAG-UP": "RUN-SHOOT-DIAG-UP",
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

class RunShootDiagUp(pState):
    def __init__(self):
        super(RunShootDiagUp, self).__init__()
        self.animation = Spritesheet(PLAYER_SPRITES_PATH + 'RunShootDiagUp-player.png', (96,96)).get_animation(0,0,64,64,6,(255,0,0))
        self.posibleNexts = {
            "JUMP": "JUMP-SHOOTING",
            "RUN_LEFT": "RUN-SHOOT",
            "RUN_RIGHT": "RUN-SHOOT",
            "IDLE": "IDLE-SHOOT",
            "SHOOT": "RUN-SHOOT",
            "SHOOT-DOWN": "RUN-SHOOT-DOWN",
            "SHOOT-UP": "RUN-SHOOT-UP",
            "SHOOT-DIAG-DOWN":"RUN-SHOOT-DIAG-DOWN",
            "SHOOT-DIAG-UP": "RUN-SHOOT-DIAG-UP",
            "STOP-SHOOT": "RUN",
        }

class RunShootDiagDown(pState):
    def __init__(self):
        super(RunShootDiagDown, self).__init__()
        self.animation = Spritesheet(PLAYER_SPRITES_PATH + 'RunShootDiagDown-player.png', (96,96)).get_animation(0,0,64,64,6,(255,0,0))
        self.posibleNexts = {
            "JUMP": "JUMP-SHOOTING",
            "RUN_LEFT": "RUN-SHOOT",
            "RUN_RIGHT": "RUN-SHOOT",
            "IDLE": "IDLE-SHOOT",
            "SHOOT": "RUN-SHOOT",
            "SHOOT-DOWN": "RUN-SHOOT-DOWN",
            "SHOOT-UP": "RUN-SHOOT-UP",
            "SHOOT-DIAG-DOWN":"RUN-SHOOT-DIAG-DOWN",
            "SHOOT-DIAG-UP": "RUN-SHOOT-DIAG-UP",
            "STOP-SHOOT": "RUN",
        }


class RunShootDown(pState):
    def __init__(self):
        super(RunShootDown, self).__init__()
        self.animation = Spritesheet(PLAYER_SPRITES_PATH + 'RunShootDown-player.png', (96,96)).get_animation(0,0,64,64,6,(255,0,0))
        self.posibleNexts = {
            "JUMP": "JUMP-SHOOTING",
            "RUN_LEFT": "RUN-SHOOT",
            "RUN_RIGHT": "RUN-SHOOT",
            "IDLE": "IDLE-SHOOT",
            "SHOOT": "RUN-SHOOT",
            "SHOOT-DOWN": "RUN-SHOOT-DOWN",
            "SHOOT-UP": "RUN-SHOOT-UP",
            "SHOOT-DIAG-DOWN":"RUN-SHOOT-DIAG-DOWN",
            "SHOOT-DIAG-UP": "RUN-SHOOT-DIAG-UP",
            "STOP-SHOOT": "RUN",
        }


class RunShootUp(pState):
    def __init__(self):
        super(RunShootUp, self).__init__()
        self.animation = Spritesheet(PLAYER_SPRITES_PATH + 'RunShootUp-player.png', (96,96)).get_animation(0,0,64,64,6,(255,0,0))
        self.posibleNexts = {
            "JUMP": "JUMP-SHOOTING",
            "RUN_LEFT": "RUN-SHOOT",
            "RUN_RIGHT": "RUN-SHOOT",
            "IDLE": "IDLE-SHOOT",
            "SHOOT": "RUN-SHOOT",
            "SHOOT-DOWN": "RUN-SHOOT-DOWN",
            "SHOOT-UP": "RUN-SHOOT-UP",
            "SHOOT-DIAG-DOWN":"RUN-SHOOT-DIAG-DOWN",
            "SHOOT-DIAG-UP": "RUN-SHOOT-DIAG-UP",
            "STOP-SHOOT": "RUN",
        }