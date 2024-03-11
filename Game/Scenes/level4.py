import pygame
from Constants.constants import *
from Entities.Enemies.randomEnemyFactorySecuence import RandomEnemyFactorySecuence
from Game.Scenes.scene import Scene
from Entities.Player.player import Player
import Game.Scenes.game_over as game_over
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
from UI.uiBossHealthBar import UIBossHealthBar


class Level4(Scene):
    def __init__(self, director, offset, dificulty):
        super(Level4, self).__init__(director)
        self.cameraOffset = offset
        self.dificulty = dificulty
        self.enemies_group = pygame.sprite.Group()
        self.interactiveGroup = pygame.sprite.Group()

        self.healthPickUps = pygame.sprite.Group()
        self.destructibles_group = pygame.sprite.Group()
        self.grenades_group = pygame.sprite.Group()
        self.bullets_group = pygame.sprite.Group()
        self.back_animations_group = pygame.sprite.Group()
        self.front_animations_group = pygame.sprite.Group()
        self.gunPickups = pygame.sprite.Group()
        self.triggerGroup = pygame.sprite.Group()

        self.uiText = UIText()
        self.uiHearts = UIHearts()
        self.uiEnergy = UIEnergy()
        self.uiCounter = UICounter()
        self.healthBar = UIBossHealthBar()
        self.randomEnemyFactory = RandomEnemyFactory(self.bullets_group, self.grenades_group,self.healthBar)
        self.randomEnemyFactorySecuence = RandomEnemyFactorySecuence(self.enemies_group, self.dificulty, self.uiCounter)

        self.world = World("Lvl4", self.enemies_group, self.randomEnemyFactory, self.randomEnemyFactorySecuence,self.interactiveGroup, self.cameraOffset, self.healthPickUps,self.destructibles_group, self.gunPickups, self.triggerGroup,self.dificulty)
        self.world.inicialOffset(self.cameraOffset)

        self.player = Player(self.screen_rect.center[0], self.screen_rect.center[1],self.uiHearts,self.uiText, self.dificulty)
        self.ui = Ui(self.player, self.uiText, self.uiHearts,self.uiEnergy, self.uiCounter,self.healthBar)
        
        self.enemies_group.update(1, self.world, self.player, self.cameraOffset, self.enemies_group)
        self.interactiveGroup.update(self.cameraOffset)
        self.healthPickUps.update(self.player, self.cameraOffset, self.healthPickUps)
        self.back_animations_group.update(self.cameraOffset, self.back_animations_group)
        self.destructibles_group.update(self.cameraOffset)
        self.gunPickups.update(self.cameraOffset)
        self.triggerGroup.update(self.cameraOffset)

    def manageJoystick(self, joystick):
        if joystick.get_axis(0) < -0.5:
            self.player.move_left()
        if joystick.get_axis(0) > 0.5:
            self.player.move_right()
        if joystick.get_button(2):
            self.player.jump()
        if joystick.get_axis(2) > 0.5 and joystick.get_axis(3) < -0.5:
            self.player.shoot(45)
        if joystick.get_axis(2) < -0.5 and joystick.get_axis(3) < -0.5:
            self.player.shoot(135)
        if joystick.get_axis(2) > 0.5 and joystick.get_axis(3) > 0.5:
            self.player.shoot(315)
        if joystick.get_axis(2) < -0.5 and joystick.get_axis(3) > 0.5:
            self.player.shoot(225)
        if joystick.get_axis(2) > 0.5:
            self.player.shoot(0)
        if joystick.get_axis(2) < -0.5:
            self.player.shoot(180)
        if joystick.get_axis(3) < -0.5:
            self.player.shoot(90)
        if joystick.get_axis(3) > 0.5:
            self.player.shoot(270)
        if joystick.get_button(3):
            self.player.cover()
        if joystick.get_button(4):
            self.player.launchGrenade(135,self.grenades_group)
        if joystick.get_button(5):
            self.player.launchGrenade(45,self.grenades_group)
        if joystick.get_button(0):
            self.player.doInteract(self.interactiveGroup)
        # if not keys[pygame.K_a] and not keys[pygame.K_d] and not keys[pygame.K_SPACE]:
        #     self.player.idle()
        # if not keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
        #     self.player.stopShooting()

    def events(self, events, keys, joysticks):
        for event in events:
            if event.type == pygame.QUIT:
                self.director.endApplication()
    
        for joystick in joysticks.values():
            self.manageJoystick(joystick)
        
        if not keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.player.stopShooting()
        if not keys[pygame.K_a] and not keys[pygame.K_d] and not keys[pygame.K_SPACE]:
            self.player.idle()
        if keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            self.player.shoot(45, self.bullets_group)
        if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            self.player.shoot(135,self.bullets_group)
        if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            self.player.shoot(315,self.bullets_group)
        if keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
            self.player.shoot(225,self.bullets_group)
        if keys[pygame.K_RIGHT]:
            self.player.shoot(0,self.bullets_group)
        if keys[pygame.K_LEFT]:
            self.player.shoot(180,self.bullets_group)
        if keys[pygame.K_UP]:
            self.player.shoot(90,self.bullets_group)
        if keys[pygame.K_DOWN]:
            self.player.shoot(270,self.bullets_group)
        if keys[pygame.K_a]:
            self.player.move_left()
        if keys[pygame.K_d]:
            self.player.move_right()
        if keys[pygame.K_SPACE]:
            self.player.jump()
        if keys[pygame.K_f]:
            self.player.cover()
        if keys[pygame.K_g]:
            self.player.launchGrenade(135,self.grenades_group)
        if keys[pygame.K_h]:
            self.player.launchGrenade(45,self.grenades_group)
        if keys[pygame.K_e]:
            self.player.doInteract(self.interactiveGroup)

    def update(self, dt):
        self.cameraOffset = self.player.update(self.world, dt, self.enemies_group, self.interactiveGroup, self.triggerGroup, self.cameraOffset)
        self.enemies_group.update(dt, self.world, self.player, self.cameraOffset,self.enemies_group)
        self.interactiveGroup.update(self.cameraOffset)
        self.healthPickUps.update(self.player, self.cameraOffset, self.healthPickUps)
        self.grenades_group.update(self.cameraOffset, dt, self.world, self.enemies_group, self.destructibles_group, self.grenades_group,self.back_animations_group)
        self.bullets_group.update(self.cameraOffset, dt, self.world, self.enemies_group, self.destructibles_group, self.bullets_group, self.back_animations_group)
        self.back_animations_group.update(self.cameraOffset, self.back_animations_group)
        self.destructibles_group.update(self.cameraOffset)
        self.gunPickups.update(self.cameraOffset)

        for gun in self.gunPickups:
            if gun.collidesWithPlayer(self.player, self.gunPickups):
                self.player = gun.getPlayerWithIt(self.player,self.ui)

        # Si se queda sin vidas acaba el juego
        if self.player.getHp() <= 0:
            scene = game_over.GameOver(self.director)
            self.director.changeScene(scene)

        for trigger in self.triggerGroup:
            text = trigger.update(self.cameraOffset)
            if text != "":
                if text == "lvl2":
                    scene = lvl2.Level2(self.director, LVL4_TO_LVL2, self.dificulty)
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
        self.bullets_group.draw(surface)
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