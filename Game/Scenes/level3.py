import pygame
from Constants.constants import *
from Entities.Enemies.randomEnemyFactorySecuence import RandomEnemyFactorySecuence
from Game.Scenes.scene import Scene
from Entities.Player.player import Player
import Game.Scenes.game_over as game_over
import Game.Scenes.level as level
import Game.Scenes.level1 as lvl1
import Game.Scenes.level2 as lvl2
import Game.Scenes.level3 as lvl3
import Game.Scenes.level4 as lvl4
from Game.world import World
from UI.ui import Ui
from Entities.Enemies.randomEnemyFactory import RandomEnemyFactory
from UI.uiCounter import UICounter
from UI.uiText import UIText
from UI.uiHearts import UIHearts
from UI.uiEnergy import UIEnergy
from UI.uiCounter import UICounter
from Entities.Player.playerWithShield import PlayerWithShield
from Entities.Player.playerWithGrenadeLauncher import PlayerWithGrenadeLauncher


class Level3(level.Level):
    def __init__(self, director, offset, dificulty):
        super(Level3, self).__init__(director, offset, dificulty)

        self.world = World("Lvl3", self.enemies_group, self.randomEnemyFactory, self.randomEnemyFactorySecuence,self.interactiveGroup, self.cameraOffset, self.healthPickUps,self.destructibles_group, self.gunPickups, self.triggerGroup,self.dificulty)
        self.world.inicialOffset(self.cameraOffset)
        
        self.enemies_group.update(1, self.world, self.player, self.cameraOffset, self.enemies_group)
        self.interactiveGroup.update(self.cameraOffset)
        self.healthPickUps.update(self.player, self.cameraOffset, self.healthPickUps)
        self.back_animations_group.update(self.cameraOffset, self.back_animations_group)
        self.destructibles_group.update(self.cameraOffset)
        self.gunPickups.update(self.cameraOffset)
        self.triggerGroup.update(self.cameraOffset)

    def manageJoystick(self, joystick):
        super(Level3, self).manageJoystick(joystick)

    def events(self, events, keys, joysticks):
        super(Level3, self).events(events, keys, joysticks)

    def update(self, dt):
        super(Level3, self).update(dt)
        for trigger in self.triggerGroup:
            text = trigger.update(self.cameraOffset)
            if text != "":
                if text == "lvl2":
                    scene = lvl2.Level2(self.director, LVL3_TO_LVL2, self.dificulty)
                    self.director.changeScene(scene)
                if text == "lvl2Vent":
                    scene = lvl2.Level2(self.director, LVL3_TO_LVL2_ALTER, self.dificulty)
                    self.director.changeScene(scene)


        #if self.player.checkInteractuable(self.world):
            #self.text.showInteractuableText("Presiona E para interactuar.", "white")
            
    def draw(self, surface):
        surface.fill("black")
        self.world.draw(surface, self.cameraOffset)
        self.destructibles_group.draw(surface)
        self.player.draw(surface)
        self.enemies_group.draw(surface)
        self.ui.draw(surface)
        self.interactiveGroup.draw(surface)
        self.healthPickUps.draw(surface)
        self.grenades_group.draw(surface)
        self.gunPickups.draw(surface)
        self.triggerGroup.draw(surface)

        #for interactive in self.interactiveGroup:
            #interactive.draw2(surface)
        #for grenade in self.grenades_group:
            #grenade.draw(surface)
        for animation in self.back_animations_group:
            animation.draw(surface)

        #self.text.draw(surface)
        for enemy in self.enemies_group:
            enemy.drawBullets(surface)
        #for enemy in self.enemies_group:
        #     #pygame.draw.rect(surface, (255,0,0), enemy.visionLine)
        #     #print(enemy.lineStart)
            #pygame.draw.line(surface, "red", enemy.lineStart, (self.player.position().centerx, self.player.position().centery), 5)
            #enemy.drawBullets(surface)