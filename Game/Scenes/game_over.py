import pygame
from .scene import Scene
import Game.Scenes.menu as menu

class GameOver(Scene):
    def __init__(self,director):
        super(GameOver, self).__init__(director)
        self.title = self.font.render("Game Over", True, pygame.Color("white"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.instructions = self.font.render("Presiona espacio para volver a empezar, o enter para ir al menu",
                                             True, pygame.Color("white"))
        instructions_center = (self.screen_rect.center[0], self.screen_rect.center[1] + 50)
        self.instructions_rect = self.instructions.get_rect(center=instructions_center)

    def events(self, events, keys, joysticks):
        for event in events:
            if event.type == pygame.QUIT:
                self.director.endApplication()
        for joystick in joysticks.values():
            joystick.get_numhats()
        if keys[pygame.K_RETURN] or joystick.get_button(9):  
            scene = menu.Menu(self.director)
            self.director.changeScene(scene)
        if keys[pygame.K_SPACE] or joystick.get_button(2):
            self.director.finishScene()
        if keys[pygame.K_ESCAPE]:
            self.director.endApplication()
    
    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.title, self.title_rect)
        surface.blit(self.instructions, self.instructions_rect)