import pygame
from Game.GameStates.base import State
from Entities.Player.player import Player
from Game.world import World
from UI.ui import Ui
from Entities.Player.pistol import Pistol
from Entities.Enemies.randomEnemyFactory import RandomEnemyFactory
from UI.uiText import UIText
from UI.uiHearts import UIHearts
# El gameplay seria buena idea hacerlo observador de player? 

class Gameplay(State):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.next_state = "GAME_OVER"
        self.cameraOffset = (1000,0)
        
        self.randomEnemyFactory = RandomEnemyFactory()
        self.enemies_group = pygame.sprite.Group()
        self.interactiveGroup = pygame.sprite.Group()


        self.player = Player(self.screen_rect.center[0], self.screen_rect.center[1])
        
        self.world = World(self.enemies_group, self.randomEnemyFactory, self.interactiveGroup, self.cameraOffset)

        self.world.inicialOffset((2600,220))
        
        self.uiText = UIText()
        self.uiHearts = UIHearts()
        self.ui = Ui(self.player, self.uiText, self.uiHearts)

        self.player.addObserver(self.uiText)
        self.player.addObserver(self.uiHearts)
        self.player = Pistol(self.player)


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
            self.player.shoot(180)
        if keys[pygame.K_RIGHT]:
            self.player.shoot(0)
        if keys[pygame.K_UP]:
            self.player.shoot(90)
        if keys[pygame.K_DOWN]:
            self.player.shoot(270)

                
        
        self.cameraOffset = self.player.update(self.world, dt, self.enemies_group, self.interactiveGroup, self.cameraOffset)
        self.enemies_group.update(self.world, self.player)
        self.interactiveGroup.update(self.player)
        
        # Si se queda sin vidas acaba el juego
        if self.player.getHp() <= 0: 
            self.done = True
        
        if self.player.checkGunPick(self.world):
            self.player = Pistol(self.player)
        
        #if self.player.checkInteractuable(self.world):
            #self.text.showInteractuableText("Presiona E para interactuar.", "white")
            
    def draw(self, surface):
        surface.fill("gray")
        self.world.draw(surface, self.cameraOffset)
        self.player.draw(surface)
        self.enemies_group.draw(surface)
        self.ui.draw(surface)
        self.interactiveGroup.draw(surface)
        #self.text.draw(surface)
        
        for enemy in self.enemies_group:
            #pygame.draw.rect(surface, (255,0,0), enemy.visionLine)
            #print(enemy.lineStart)
            pygame.draw.line(surface, "red", enemy.lineStart, (self.player.position().centerx, self.player.position().centery), 5)
            enemy.drawBullets(surface)

        
            
            
            
