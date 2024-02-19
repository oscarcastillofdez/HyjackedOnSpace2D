import pygame
from .base import State
from player import Player
from world import World
from ui import Ui

class Gameplay(State):
    def __init__(self, gv):
        super(Gameplay, self).__init__()
        self.next_state = "GAME_OVER"
        self.globalVars = gv
        self.enemies_group = pygame.sprite.Group()
        self.world = World(gv, self.enemies_group )
        self.player = Player(self.screen_rect.center[0], self.screen_rect.center[1])
        self.ui = Ui()

    def get_event(self, event):
        if event.type == pygame.QUIT:
                self.quit = True
        


    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
                self.player.move_left()
        if keys[pygame.K_d]:
                self.player.move_right()
        if keys[pygame.K_SPACE]:
                self.player.jump()
        self.player.update(self.world, self.globalVars, dt)
        self.enemies_group.update(self.world)
        # Si toca un enemigo se acaba el juego
        if pygame.sprite.spritecollide(self.player, self.enemies_group, False):
            if self.player.checkHit() == True:
                self.done = True
            self.ui.updateHealthHearts(self.player)
            
            print(self.player.healthPoints)
        
        
        
    
    def draw(self, surface):
        surface.fill("gray")
        self.player.draw(surface)
        self.world.draw(surface, self.globalVars)
        self.enemies_group.draw(surface)
        self.ui.draw(surface)