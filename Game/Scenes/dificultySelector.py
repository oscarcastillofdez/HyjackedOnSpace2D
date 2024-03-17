import pygame

from Constants.constants import *
from Game.Scenes.level3 import Level3
from Game.Scenes.level4 import Level4
from Game.easyMode import EasyMode
from Game.hardMode import HardMode
from Game.mediumMode import MediumMode
from .scene import Scene
from .level1 import Level1
import Entities.Player.player as player
import UI.uiText as uiText
import UI.uiHearts as uiHearts
import UI.uiEnergy as uiEnergy
import UI.uiCounter as uiCounter
import UI.uiHealthBar as uiHealthBar
import UI.uiPistolIcon as uiPistol
import UI.uiPistolUpgradedIcon as uiPistolUpgrade
import UI.uiGrenadeLauncherIcon as uiGrenade
import UI.uiRahmCroshair as uiRahmCroshair
import UI.uiDash as uiDash

class DificultySelector(Scene):
    def __init__(self,director):
        super(DificultySelector, self).__init__(director)
        self.active_index = 0
        self.options = ["Easy", "Medium", "Hard"]
    
    # Funcion renderiza el texto del menu, pone azul la opcion que 
    # se esta seleccionando
    def render_text(self, index):
        color = pygame.Color("blue") if index == self.active_index else pygame.Color("white")
        return self.font.render(self.options[index], True, color)
    
    def get_text_position(self, text, index):
        center = (self.screen_rect.center[0], self.screen_rect.center[1] + (index * 50))
        return text.get_rect(center=center)
    
    def handle_action(self):
        uitext = uiText.UIText()
        uihearts = uiHearts.UIHearts()
        uienergy = uiEnergy.UIEnergy()
        uicroshair = uiRahmCroshair.UIRahmCroshair()
        uipistol = uiPistol.UIPistol()
        uipistolUpgrade = uiPistolUpgrade.UIPistolUpgrade()
        uigrenadeLauncher = uiGrenade.UIGrenadeLauncher()
        uidash = uiDash.UIDash()

        self.persist = {
                        'player': None,
                        'checkpoint': INIT_OFFSET,
                        'dificulty': None,
                        'uienergy': uienergy,
                        'UIPistol': uipistol,
                        'uipistolupgrade': uipistolUpgrade,
                        'UIGrenadeLauncher': uigrenadeLauncher,
                        'UIDash': uidash
                    }
        if self.active_index == 0:
            dificulty = EasyMode()  
            playerObj = player.Player(self.screen_rect.center[0], self.screen_rect.center[1], dificulty, uitext, uihearts)    
            self.persist['player'] = playerObj
            self.persist['dificulty'] = dificulty
            scene = Level1(self.director, INIT_OFFSET, dificulty, playerObj, uienergy, uipistol, uipistolUpgrade, uigrenadeLauncher, uidash, self.persist)
            scene.startup()
            self.director.stackScene(scene)
        elif self.active_index == 1:
            dificulty = MediumMode()
            playerObj = player.Player(self.screen_rect.center[0], self.screen_rect.center[1], dificulty, uitext, uihearts)
            self.persist['player'] = playerObj
            self.persist['dificulty'] = dificulty
            scene = Level1(self.director,INIT_OFFSET, dificulty, playerObj, uienergy, uipistol, uipistolUpgrade, uigrenadeLauncher, uidash, self.persist)
            scene.startup()
            self.director.stackScene(scene)
        elif self.active_index == 2:
            dificulty = HardMode()
            playerObj = player.Player(self.screen_rect.center[0], self.screen_rect.center[1], dificulty, uitext, uihearts)
            self.persist['player'] = playerObj
            self.persist['dificulty'] = dificulty
            scene = Level1(self.director,INIT_OFFSET, dificulty, playerObj, uienergy, uipistol, uipistolUpgrade, uigrenadeLauncher, uidash, self.persist)
            scene.startup()
            self.director.stackScene(scene)
    
    # Maneja la transicion entre las opciones del menu
    def events(self, events, keys, joysticks):
        for event in events:
            if event.type == pygame.QUIT:
                self.director.endApplication()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.active_index -= 1 if self.active_index >= 1 else 0
                elif event.key == pygame.K_DOWN:
                    self.active_index += 1 if self.active_index < 2 else 0
                elif event.key == pygame.K_RETURN:
                    self.handle_action()
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 2:
                    self.handle_action()
            for joystick in joysticks.values():
                hats = joystick.get_numhats()
                for i in range(hats):
                    hat = joystick.get_hat(i)
                    if hat[1] == 1:
                        self.active_index -= 1 if self.active_index >= 1 else 0
                    if hat[1] == -1:
                        self.active_index += 1 if self.active_index < 2 else 0

    def update(self, *args):
        pass 
    
    def draw(self, surface):
        spaceBackground = pygame.transform.scale(pygame.image.load(LVLS_PATH + '/space2.jpg'), (SCREEN_WIDTH,SCREEN_HEIGTH)).convert()
        spaceBackgroundRect = spaceBackground.get_rect()
        surface.blit(spaceBackground,spaceBackgroundRect)
        #self.music.play()
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(text_render, index))