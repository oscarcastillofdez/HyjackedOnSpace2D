import pygame
from Constants.constants import *
from Entities.Enemies.randomEnemyFactorySecuence import RandomEnemyFactorySecuence
from Game.Scenes.scene import Scene
from Entities.Player.player import Player
import Game.Scenes.game_over as game_over
import Game.Scenes.level as level
import Game.Scenes.level2 as lvl2
import Game.Scenes.level3 as lvl3
import Game.Scenes.level4 as lvl4
from Game.world import World
from UI.ui import Ui
from UI.uiCounter import UICounter
from UI.uiText import UIText
from UI.uiHearts import UIHearts
from UI.uiEnergy import UIEnergy
from UI.uiCounter import UICounter
from Entities.Player.playerWithShield import PlayerWithShield
from Entities.Player.playerWithGrenadeLauncher import PlayerWithGrenadeLauncher
from UI.uiHealthBar import UIBossHealthBar


class Level1(level.Level):
    def __init__(self, director, offset, dificulty, player, uienergy, uipistol, uipistolUpgrade, uigrenadeLauncher,uidash, persist):
        super(Level1, self).__init__(director, offset, dificulty, player, uienergy, uipistol, uipistolUpgrade, uigrenadeLauncher,uidash, persist)

        boss = True
        if self.persist['checkpoint'] == CHECKPOINT_LVL1 or self.persist['checkpoint'] == CHECKPOINT_LVL3:
            boss = False
        
        pistol = self.persist['pistolPick']
        pistolUpgrade = self.persist['pistolPick']
        shield = self.persist['pistolPick']

        self.world = World("Lvl1", self.enemies_group, self.randomEnemyFactory, self.randomEnemyFactorySecuence,self.interactiveGroup, self.cameraOffset, self.healthPickUps,self.destructibles_group, self.gunPickups, self.triggerGroup,self.dificulty, boss, pistol, pistolUpgrade, shield)
        self.world.inicialOffset(self.cameraOffset)
        
        self.enemies_group.update(1, self.world, self.player, self.cameraOffset, self.enemies_group)
        self.interactiveGroup.update(self.cameraOffset)
        self.healthPickUps.update(self.player, self.cameraOffset, self.healthPickUps)
        self.back_animations_group.update(self.cameraOffset, self.back_animations_group)
        self.destructibles_group.update(self.cameraOffset)
        self.gunPickups.update(self.cameraOffset)
        self.triggerGroup.update(self.cameraOffset)

        self.music = 'Assets/Audio/RatchetAndClank_QwarkHideout.mp3'
        



    def manageJoystick(self, joystick):
        super(Level1, self).manageJoystick(joystick)

    def events(self, events, keys, joysticks):
        super(Level1, self).events(events, keys, joysticks)

    def update(self, dt):
        super(Level1, self).update(dt)

        for trigger in self.triggerGroup:
            text = trigger.update(self.cameraOffset)
            if text != "":
                if text == "lvl2":
                    self.player.resetPlayerPos()
                    scene = lvl2.Level2(self.director, LVL1_TO_LVL2, self.dificulty, self.player, self.uiEnergy, self.uiPistol, self.uiPistolUpgrade, self.uiGrenadeLauncher,self.uiDash, self.persist)
                    scene.startup()
                    self.director.changeScene(scene)


        #if self.player.checkInteractuable(self.world):
            #self.text.showInteractuableText("Presiona E para interactuar.", "white")
            
    def draw(self, surface):
        super(Level1, self).draw(surface)