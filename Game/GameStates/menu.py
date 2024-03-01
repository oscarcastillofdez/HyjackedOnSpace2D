import pygame
from .base import State

class Menu(State):
    def __init__(self):
        super(Menu, self).__init__()
        self.active_index = 0
        self.options = ["Play", "Options", "Quit"]
        self.next_state = "GAMEPLAY"
        self.music = pygame.mixer.Sound('Assets/Audio/MainMenu.mp3')
    
    # Funcion renderiza el texto del menu, pone azul la opcion que 
    # se esta seleccionando
    def render_text(self, index):
        color = pygame.Color("blue") if index == self.active_index else pygame.Color("white")
        return self.font.render(self.options[index], True, color)
    
    def get_text_position(self, text, index):
        center = (self.screen_rect.center[0], self.screen_rect.center[1] + (index * 50))
        return text.get_rect(center=center)
    
    def handle_action(self):
        if self.active_index == 0:
            self.done = True
        elif self.active_index == 1:
            self.done = True
            self.next_state = "OPTIONS"
        elif self.active_index == 2:
            self.quit = True
    
    # Maneja la transicion entre las opciones del menu
    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.active_index -= 1 if self.active_index >= 1 else 0
                print(self.active_index)
            elif event.key == pygame.K_DOWN:
                self.active_index += 1 if self.active_index < 2 else 0
                print(self.active_index)
            elif event.key == pygame.K_RETURN:
                self.handle_action()

    
    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        #self.music.play()
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(text_render, index))