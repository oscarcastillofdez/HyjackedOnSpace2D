from pygame import Rect
from .enemyFactory import EnemyFactory
from .flyingEnemy import FlyingEnemy
from .wallDestructible import WallDestructible
from .enemy import Enemy
import random
from Constants.constants import *

class RandomEnemyFactorySecuence(EnemyFactory):
    def __init__(self,x,y, enemiesGroup) -> None:
        self.enemiesGroup = enemiesGroup

        #self.spawnArea = Rect(x,y,1000,500)
        self.spawnArea = Rect(x,y,500,500)
        #self.spawnArea.x = random.randrange(-100, -40)
        #self.spawnArea.y = random.randrange(0, SCREEN_HEIGTH)
        
        self.enemySpawnRate = 100

    def activate(self, spawnCenterX, spawnCenterY):
        #self.spawnArea.x = spawnCenterX - 1000
        #self.spawnArea.y = spawnCenterY - 500

        self.spawnArea.x = spawnCenterX
        self.spawnArea.y = spawnCenterY - 500
        spawnPointX = random.randrange(self.spawnArea.x, self.spawnArea.x + 500)
        spawnPointY = random.randrange(self.spawnArea.y, self.spawnArea.y + 500)

        selectEnemy = random.randint(0, 1)
        if selectEnemy == 0:
            en = Enemy(spawnPointX, spawnPointY)
            self.enemiesGroup.add(en)
        elif selectEnemy == 1:
            en = FlyingEnemy(spawnPointX, spawnPointY)
            self.enemiesGroup.add(en)
        