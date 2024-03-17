import pygame
from .scene import Scene
from .menu import Menu
from Constants.constants import *
"""
    Este estado es la pantalla de carga, cuando inicias el juego
    tiene el titulo del juego.
"""

class Splash(Scene):
    def __init__(self, director):
        super(Splash, self).__init__(director)
        self.title = self.font.render("Hyjacked On Space 2D", True, pygame.Color("blue"))
        self.title_rect = self.title.get_rect(center = self.screen_rect.center)
        self.time_active = 0
        self.font = pygame.font.Font("Assets/Fonts/Cyberverse Oblique.ttf", 42)
    
    def events(self, *args):
        # No hacemos nada porque no hay que hacer nada
        pass

    def update(self, dt):
        self.time_active += dt
        if self.time_active >= 1000:
            scene = Menu(self.director)
            scene.startup()
            self.director.changeScene(scene)
    
    def draw(self, surface):
        spaceBackground = pygame.transform.scale(pygame.image.load(LVLS_PATH + '/space2.jpg'), (SCREEN_WIDTH,SCREEN_HEIGTH)).convert()
        spaceBackgroundRect = spaceBackground.get_rect()
        surface.blit(spaceBackground,spaceBackgroundRect)
        surface.blit(self.title, self.title_rect)
