import pygame
from .base import State
from player import Player
from world import World
from ui import Ui
from pistol import Pistol
# El gameplay seria buena idea hacerlo observador de player? 

class Gameplay(State):
    def __init__(self, gv):
        super(Gameplay, self).__init__()
        self.next_state = "GAME_OVER"
        self.globalVars = gv
        self.enemies_group = pygame.sprite.Group()
        self.player = Player(self.screen_rect.center[0], self.screen_rect.center[1])
        self.world = World(gv, self.enemies_group)
        

        self.ui = Ui(self.player)

        self.player.addObserver(self.ui)

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
        if keys[pygame.K_LEFT]:
            self.player.shoot("left", self.globalVars)
        if keys[pygame.K_RIGHT]:
            self.player.shoot("right", self.globalVars)
        if keys[pygame.K_UP]:
            self.player.shoot("up", self.globalVars)
        if keys[pygame.K_DOWN]:
            self.player.shoot("down", self.globalVars)
                
        self.player.update(self.world, self.globalVars, dt, self.enemies_group)
        self.enemies_group.update(self.world)
        
        # Si se queda sin vidas acaba el juego
        if self.player.getHp() <= 0: 
            self.done = True
        
        #self.player.disparar()
        if self.player.checkGunPick(self.world):
            self.player = Pistol(self.player)

    
    def draw(self, surface):
        surface.fill("gray")
        self.player.draw(surface)
        self.world.draw(surface, self.globalVars)
        self.enemies_group.draw(surface)
        self.ui.draw(surface)
        