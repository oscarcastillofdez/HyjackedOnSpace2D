import pygame
from .base import State

class GameOver(State):
    def __init__(self):
        super(GameOver, self).__init__()
        self.title = self.font.render("Game Over", True, pygame.Color("white"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.instructions = self.font.render("Presiona espacio para volver a empezar, o enter para ir al menu",
                                             True, pygame.Color("white"))
        instructions_center = (self.screen_rect.center[0], self.screen_rect.center[1] + 50)
        self.instructions_rect = self.instructions.get_rect(center=instructions_center)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                self.next_state = "MENU"
                self.done = True
            elif event.key == pygame.K_SPACE:
                self.next_state = "GAMEPLAY"
                self.done = True
            elif event.key == pygame.K_SPACE:
                self.quit = True
    
    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.title, self.title_rect)
        surface.blit(self.instructions, self.instructions_rect)