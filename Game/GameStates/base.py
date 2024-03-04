"""
Funcion Estado base para implementar ejn el resto de estados 
"""

import pygame

class State(object):
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.persist = {}
        # Fuente a usar durante el juego
        # Si se quieren diferentes fuentes para diferentes
        # Estados, se pueden declarar en cada estado
        self.font = pygame.font.Font("Assets/Fonts/Airstrip_Four.ttf", 36)
    
    def startup(self, persistent):
        self.persist = persistent
    
    def get_event(self, event):
        pass
    
    def update(self, dt):
        pass

    def draw(self, surface):
        pass
    