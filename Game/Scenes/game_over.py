import pygame
from .scene import Scene
import Game.Scenes.menu as menu
import Game.Scenes.level3 as level3
import Game.Scenes.level4 as level4
import Game.Scenes.level2 as level2
import Game.Scenes.level1 as level1
import Constants.constants as c

class GameOver(Scene):
    def __init__(self,director, persist):
        super(GameOver, self).__init__(director, persist)
        self.title = self.font.render("Game Over", True, pygame.Color("white"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.instructions = self.font.render("Presiona ESPACIO para volver a empezar, o ENTER para ir al menu",
                                             True, pygame.Color("white"))
        instructions_center = (self.screen_rect.center[0], self.screen_rect.center[1] + 50)
        self.instructions_rect = self.instructions.get_rect(center=instructions_center)

    def manageJoystick(self, joystick):
        if joystick.get_button(9):  
            scene = menu.Menu(self.director)
            self.director.changeScene(scene)
        if joystick.get_button(2):
            self.director.finishScene()

    def events(self, events, keys, joysticks):
        for event in events:
            if event.type == pygame.QUIT:
                self.director.endApplication()

        for joystick in joysticks.values():
            self.manageJoystick(joystick)

        if keys[pygame.K_RETURN]:  
            scene = menu.Menu(self.director)
            self.director.changeScene(scene)
        if keys[pygame.K_SPACE]:
            self.persist['player'].resetPlayerPos()
            if self.persist['checkpoint'] == c.CHECKPOINT_LVL1:
                scene = level1.Level1(self.director, c.CHECKPOINT_LVL1,
                           self.persist['dificulty'],
                           self.persist['player'],
                           self.persist['uienergy'],
                           self.persist['UIPistol'],
                           self.persist['uipistolupgrade'],
                           self.persist['UIGrenadeLauncher'],
                           self.persist['UIDash'],
                           self.persist)
            elif self.persist['checkpoint'] == c.CHECKPOINT_LVL3:
                self.persist['uipistolupgrade'].uIHide()
                self.persist['uienergy'].hideIcon()
                scene = level3.Level3(self.director, c.CHECKPOINT_LVL3,
                            self.persist['dificulty'],
                            self.persist['player'],
                            self.persist['uienergy'],
                            self.persist['UIPistol'],
                            self.persist['uipistolupgrade'],
                            self.persist['UIGrenadeLauncher'],
                            self.persist['UIDash'],
                            self.persist)
            elif self.persist['checkpoint'] == c.INIT_OFFSET:
                self.persist['UIPistol'].uIHide()
                scene = level1.Level1(self.director, c.INIT_OFFSET,
                            self.persist['dificulty'],
                            self.persist['player'],
                            self.persist['uienergy'],
                            self.persist['UIPistol'],
                            self.persist['uipistolupgrade'],
                            self.persist['UIGrenadeLauncher'],
                            self.persist['UIDash'],
                            self.persist)
            scene.startup()
            self.director.changeScene(scene)
        if keys[pygame.K_ESCAPE]:
            self.director.endApplication()
    
    def update(self, dt):
        pass

    def draw(self, surface):
        spaceBackground = pygame.transform.scale(pygame.image.load(c.LVLS_PATH + '/space2.jpg'), (c.SCREEN_WIDTH,c.SCREEN_HEIGTH)).convert()
        spaceBackgroundRect = spaceBackground.get_rect()
        surface.blit(spaceBackground,spaceBackgroundRect)
        surface.blit(self.title, self.title_rect)
        surface.blit(self.instructions, self.instructions_rect)