import pygame
from .scene import Scene
from .level1 import Level1

class Menu(Scene):
    def __init__(self,director):
        super(Menu, self).__init__(director)
        self.active_index = 0
        self.options = ["Play", "Options", "Quit"]
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
            scene = Level1(self.director)
            self.director.stackScene(scene)
        elif self.active_index == 1:
            print("OPCIONES NO INCORPORADAS GENIO")
            #scene = Options()
            #self.director.changeScene(scene)
        elif self.active_index == 2:
            self.director.endApplication()
    
    # Maneja la transicion entre las opciones del menu
    def events(self, events, keys):
        for event in events:
            if event.type == pygame.QUIT:
                self.director.endApplication()
        if keys[pygame.K_UP]:
            self.active_index -= 1 if self.active_index >= 1 else 0
        if keys[pygame.K_DOWN]:
            self.active_index += 1 if self.active_index < 2 else 0
        if keys[pygame.K_RETURN]:
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