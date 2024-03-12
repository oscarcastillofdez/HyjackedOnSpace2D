"""
Funcion Estado base para implementar ejn el resto de estados 
"""

import pygame

class Scene(object):
    def __init__(self, director):
        self.director = director

        """self.done = False
        self.quit = False
        self.next_state = None
        """
        # Esto para que lo necesitamos?
        self.screen_rect = pygame.display.get_surface().get_rect()

        self.persist = {}
        # Fuente a usar durante el juego
        # Si se quieren diferentes fuentes para diferentes
        # Escenas, se pueden declarar en cada escena
        self.font = pygame.font.Font("Assets/Fonts/Airstrip_Four.ttf", 36)
        self.music = 'Assets/Audio/MainMenu.mp3'
    
    def startup(self, persistent={}):
        self.persist = persistent
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play(-1)
    
    def update(self, *args):
        raise NotImplemented("Tiene que implementar el metodo update.")
    
    def events(self, *args):
        raise NotImplemented("Tiene que implementar el metodo events.")

    def draw(self, surface):
        raise NotImplemented("Tiene que implementar el metodo draw.")
    