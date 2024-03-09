import pygame
import Game.Scenes.menu as menu


from Game.easyMode import EasyMode
from Game.hardMode import HardMode
from Game.mediumMode import MediumMode
from .scene import Scene
from .level1 import Level1

class PerifericSelector(Scene):
    def __init__(self,director, joystickId):
        super(PerifericSelector, self).__init__(director)
        self.active_index = 0
        self.text1 = "Se ha detectado un nuevo joystick." + str(joystickId)
        self.text2 = "La configuración ha cambiado automaticamente."
        self.text3 = "Pulsa cualquier boton para continuar."

        self.options = ["Ok"]
        self.music = pygame.mixer.Sound('Assets/Audio/MainMenu.mp3')
    
    # Funcion renderiza el texto del menu, pone azul la opcion que 
    # se esta seleccionando
    def render_text(self, index):
        color = pygame.Color("blue") if index == self.active_index else pygame.Color("white")
        return self.font.render(self.options[index], True, color)
    
    def render_text_general(self, text):
        color = pygame.Color("white")
        return self.font.render(text, True, color)
    
    def get_text_position(self, text, index):
        center = (self.screen_rect.center[0], self.screen_rect.center[1] + (index * 50))
        return text.get_rect(center=center)
    
    def get_text_general_position(self, text):
        center = (self.screen_rect.center[0], self.screen_rect.center[1])
        return text.get_rect(center=center)
    
    def handle_action(self):
        if self.active_index == 0:
            scene = menu.Menu(self.director)
            self.director.changeScene(scene)
    
    # Maneja la transicion entre las opciones del menu
    def events(self, events, keys, joysticks):
        for event in events:
            if event.type == pygame.QUIT:
                self.director.endApplication()
            if event.type == pygame.JOYBUTTONDOWN:
                self.handle_action()
        """elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.active_index -= 1 if self.active_index >= 1 else 0
                print(self.active_index)
            elif event.key == pygame.K_DOWN:
                self.active_index += 1 if self.active_index < 2 else 0
                print(self.active_index)
            elif event.key == pygame.K_RETURN:
                self.handle_action()"""

    def update(self, *args):
        pass 
    
    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        #self.music.play()
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(text_render, index))

            text1_render = self.render_text_general(self.text1)
            surface.blit(text1_render, text1_render.get_rect(center=(self.screen_rect.center[0], self.screen_rect.center[1] - 300)))

            text2_render = self.render_text_general(self.text2)
            surface.blit(text2_render, text2_render.get_rect(center=(self.screen_rect.center[0], self.screen_rect.center[1] - 200)))

            text3_render = self.render_text_general(self.text3)
            surface.blit(text3_render, text3_render.get_rect(center=(self.screen_rect.center[0], self.screen_rect.center[1] - 100)))
