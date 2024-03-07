import time
import pygame
from Constants.constants import *
from Entities.Enemies.randomEnemyFactorySecuence import RandomEnemyFactorySecuence
from UI.uiCounter import UICounter
import threading

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

        self.randomEnemyFactorySecuence = RandomEnemyFactorySecuence(x,y,enemies_group)
    
    def getCounter(self):
        return str(self.countdown)
    
    def noitify(self):
        for observer in self.observers:
            observer.update(self)
    
    def initCounter(self):
        while self.countdown > 0:
            time.sleep(1)
            self.countdown -= 1
            self.noitify()
        self.activeSecuence = False
        for observer in self.observers:
            self.observers.remove(observer)
        
    def interact(self, uiCounter):
        self.activeSecuence = True
        self.observers.append(uiCounter)
        threading.Thread(target=self.initCounter).start()

    def update(self, cameraOffset, player):
        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]

        if self.activeSecuence:
            self.spawnDelay -= 1
            if self.spawnDelay < 0:
                self.spawnDelay = 60
                self.randomEnemyFactorySecuence.createEnemy(self.rect.x, self.rect.y)

    def getText(self):
        return "Presiona E para interactuar."
    
    #def draw(self,screen):
        #self.interactiveIndicator.draw(screen)
        #pygame.draw.rect(screen, (255,255,255), self.randomEnemyFactorySecuence.spawnArea)
        