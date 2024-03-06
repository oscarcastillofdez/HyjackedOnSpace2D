import pygame
from Constants.constants import *
from Entities.Enemies.randomEnemyFactorySecuence import RandomEnemyFactorySecuence

class Computer(pygame.sprite.Sprite):
    def __init__(self,x,y,enemies_group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(INTERACTIVES_PATH + 'ibm5150.png'),(64,64))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.activeSecuence = False
        self.timeRemaining = 5000
        self.spawnDelay = 60

        self.randomEnemyFactorySecuence = RandomEnemyFactorySecuence(x,y,enemies_group)

    def interact(self):
        self.activeSecuence = True
        
        print("Interaccionaste pedrito.")

    def update(self, cameraOffset):
        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]

        if self.activeSecuence:
            self.spawnDelay -= 1
            if self.spawnDelay < 0:
                self.spawnDelay = 60
                self.timeRemaining -= 1
                if self.timeRemaining < 0:
                    self.activeSecuence = False
                else:
                    self.randomEnemyFactorySecuence.activate(self.rect.x, self.rect.y)
        
        

    def getText(self):
        return "Presiona E para interactuar."
    
    def draw2(self,screen):
        pygame.draw.rect(screen, (255,255,255), self.randomEnemyFactorySecuence.spawnArea)
        