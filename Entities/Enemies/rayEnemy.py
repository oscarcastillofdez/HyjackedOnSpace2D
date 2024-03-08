import random
import pygame
from Constants.constants import ENEMIES_PATH

from Entities.Enemies.entity import Entity
from Game.spritesheet import Spritesheet

class RayEnemy(pygame.sprite.Sprite, Entity):
    def __init__(self,x,y, onlyChase) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.spriteList = Spritesheet(ENEMIES_PATH + 'Ray/Ray_spritesheet.png', (64,256)).cargar_sprites(16,78)
        #self.image = pygame.transform.scale(pygame.image.load(ENEMIES_PATH + 'Ray/Ray_spritesheet.png'), (64,64))
        self.spriteIndex = 0
        self.image = self.spriteList[self.spriteIndex]
        self.blankImage = pygame.transform.scale(pygame.image.load(ENEMIES_PATH + 'Ray/Ray_blank.png'), (64,256))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.hidingTime = random.randint(60, 120)
        self.chasingTime = random.randint(60, 120)

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
        self.image = self.blankImage
        self.hidingTime -= 1
        if self.hidingTime < 0:
            self.chasingTime = random.randint(60, 120)
            self.current_state = "chasing"
    
    def chase(self, world, player,cameraOffset,enemies_group):
        self.spriteIndex += 1
        self.chasingTime -= 1
        if self.spriteIndex == len(self.spriteList):
            self.spriteIndex = 0
        self.image = self.spriteList[self.spriteIndex]

        if self.chasingTime < 0:
            self.hidingTime = random.randint(60, 120)
            self.current_state = "patrolling"

        if self.rect.colliderect(player.position()):
            self.current_state = "attacking"
    
    def attack(self, world, player,cameraOffset,enemies_group):
        player.hit() 
        self.current_state = "chasing"
    
    def drawBullets(self,screen):
        pass
    
    def die(self,world, player,cameraOffset,enemies_group):
        pass
    
    def kill(self):
        pass    
