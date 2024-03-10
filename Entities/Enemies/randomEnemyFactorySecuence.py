from pygame import Rect
import pygame

from Entities.Enemies.barnacleEnemy import BarnacleEnemy
from Entities.Enemies.rayEnemy import RayEnemy
from Entities.Enemies.shooterEnemy import ShooterEnemy

from .enemyFactory import EnemyFactory
from .flyingEnemy import FlyingEnemy
from .wallDestructible import WallDestructible
from .meleeEnemy import MeleeEnemy
import random
from Constants.constants import *

from math import floor

class RandomEnemyFactorySecuence(EnemyFactory):
    def __init__(self,enemiesGroup, dificulty, uiCounter) -> None:
        self.enemiesGroup = enemiesGroup
        self.dificulty = dificulty
        self.uiCounter = uiCounter

        self.spawnArea = Rect(0,0,500,500)
        self.observers = []
        
        self.maxEnemyCount = dificulty.getMaxEnemyCountOnComputerSecuence()
        self.initialCount = 0
        self.firstTick = 0
        self.timeElapsed = 0
        self.previousTime = 0
        self.countdown = dificulty.getCountdownOnComputerScene()
        self.activeSecuence = False
        self.spawnDelay = dificulty.getSpawnDelayOnComputerScene()

    def getCounter(self):
        return str(self.countdown)
    
    def noitify(self):
        for observer in self.observers:
            observer.update(self)

    def createEnemy(self, spawnCenterX, spawnCenterY):
        self.spawnArea.x = spawnCenterX + 500
        self.spawnArea.y = spawnCenterY - 500
        spawnPointX = random.randrange(self.spawnArea.x, self.spawnArea.x + 500)
        spawnPointY = random.randrange(self.spawnArea.y, self.spawnArea.y + 500)
        
        currentCount = len(self.enemiesGroup) - self.initialCount
        if currentCount < self.maxEnemyCount:
            selectEnemy = random.randint(0, 3)
            if selectEnemy == 0:
                en = MeleeEnemy(spawnPointX, spawnPointY, self.dificulty, True)
                self.enemiesGroup.add(en)
            elif selectEnemy == 1:
                en = ShooterEnemy(spawnPointX, spawnPointY, self.dificulty, True)
                self.enemiesGroup.add(en)
            elif selectEnemy == 2:
                en = BarnacleEnemy(spawnPointX, spawnPointY, self.dificulty, True)
                self.enemiesGroup.add(en)
            elif selectEnemy == 3:
                en = RayEnemy(spawnPointX, spawnPointY, self.dificulty, True)
                self.enemiesGroup.add(en)

    def activate(self):
        self.firstTick = pygame.time.get_ticks()
        self.initialCount = len(self.enemiesGroup)
        self.observers.append(self.uiCounter)
        self.activeSecuence = True

    def update(self,x,y):
        if self.activeSecuence:
            self.timeElapsed = (pygame.time.get_ticks() - self.firstTick)/1000
            self.timeElapsed = floor(self.timeElapsed)

            if self.timeElapsed != self.previousTime:
                self.previousTime = self.timeElapsed
                self.countdown -= 1
                self.noitify()
                if self.countdown == 0:
                    self.activeSecuence = False
                    for observer in self.observers:
                        self.observers.remove(observer)

            self.spawnDelay -= 1
            if self.spawnDelay < 0:
                self.spawnDelay = 60
                self.createEnemy(x, y)
        

    #def draw(self,screen):
        #self.interactiveIndicator.draw(screen)
        #pygame.draw.rect(screen, (255,255,255), self.randomEnemyFactorySecuence.spawnArea)