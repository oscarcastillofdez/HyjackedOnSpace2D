import pygame
from .base import State
from player import Player
from world import World


class Gameplay(State):
    def __init__(self, gv):
        super(Gameplay, self).__init__()
        self.next_state = "GAME_OVER"
        self.globalVars = gv
        self.enemies_group = pygame.sprite.Group()
        self.world = World(gv, self.enemies_group )
        self.player = Player(self.screen_rect.center[0] //2,self.screen_rect.center[1] //2 -130)

    def get_event(self, event):
        if event.type == pygame.QUIT:
                self.quit = True
        self.player.get_event(event)
    
    def update(self, dt):
        self.player.update(self.world, self.globalVars)
        self.enemies_group.update()
        # Si toca un enemigo se acaba el juego
        if pygame.sprite.spritecollide(self.player, self.enemies_group, False):
            self.done = True
    
    def draw(self, surface):
         surface.fill("gray")
         self.player.draw(surface)
         self.world.draw(surface, self.globalVars)
         self.enemies_group.draw(surface)