import time
import pygame
from Constants.constants import *
from Entities.Enemies.randomEnemyFactorySecuence import RandomEnemyFactorySecuence
from UI.uiCounter import UICounter
import threading
from math import floor

class Computer(pygame.sprite.Sprite):
    def __init__(self,x,y,enemies_group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(INTERACTIVES_PATH + 'ibm5150.png'),(64,64))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #self.interactiveIndicator = InteractiveIndicator(x, y)

        self.activeSecuence = False
        self.spawnDelay = 60
        self.observers = []
        self.countdown = 60
        self.previousTime = 0
        self.timeElapsed = 0
        self.randomEnemyFactorySecuence = RandomEnemyFactorySecuence(x,y,enemies_group)
    
    def getCounter(self):
        return str(self.countdown)
    
    def noitify(self):
        for observer in self.observers:
            observer.update(self)
        
    def interact(self, uiCounter):
        self.activeSecuence = True
        self.observers.append(uiCounter)
        self.firstTick = pygame.time.get_ticks()

    def update(self, cameraOffset, player):
        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]

        if self.activeSecuence:
            self.timeElapsed = (pygame.time.get_ticks() - self.firstTick)/1000
            self.timeElapsed = floor(self.timeElapsed)

            if self.timeElapsed != self.previousTime:
                self.previousTime = self.timeElapsed
                self.countdown -= 1
                self.noitify()
                if self.countdown == 0:
                    self.activeSecuence = False

            self.spawnDelay -= 1
            if self.spawnDelay < 0:
                self.spawnDelay = 60
                self.randomEnemyFactorySecuence.createEnemy(self.rect.x, self.rect.y)

    def getText(self):
        return "Presiona E para interactuar."
    
    #def draw(self,screen):
        #self.interactiveIndicator.draw(screen)
        #pygame.draw.rect(screen, (255,255,255), self.randomEnemyFactorySecuence.spawnArea)
        