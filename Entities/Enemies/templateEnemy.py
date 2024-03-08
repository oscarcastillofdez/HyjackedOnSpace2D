import pygame
from Constants.constants import ENEMIES_PATH

from Entities.Enemies.entity import Entity

class Enemy(pygame.sprite.Sprite, Entity):
    def __init__(self,x,y, onlyChase) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(ENEMIES_PATH + 'Barnacle.png'), (64,64))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.states = {"patrolling": self.patrol,
                       "chasing": self.chase,
                       "attacking": self.attack,
                       "die": self.die}
        self.current_state = "patrolling"
    
    def update(self, dt, world, player,cameraOffset, enemies_group):
        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]

        self.states[self.current_state](world, player, cameraOffset, enemies_group) # Llama al estado correspondiente (patrol, chase o attack)

    def patrol(self, world, player,cameraOffset,enemies_group):
        pass
    
    def chase(self, world, player,cameraOffset,enemies_group):
        pass

    def die(self,world, player,cameraOffset,enemies_group):
        pass
    
    def attack(self, world, player,cameraOffset,enemies_group):
        pass
    
    def drawBullets(self,screen):
        pass
    
    def kill(self):
        pass 
    
