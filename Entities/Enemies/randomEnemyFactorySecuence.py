from pygame import Rect

from .enemyFactory import EnemyFactory
from .flyingEnemy import FlyingEnemy
from .wallDestructible import WallDestructible
from .meleeEnemy import MeleeEnemy
import random
from Constants.constants import *

class RandomEnemyFactorySecuence(EnemyFactory):
    def __init__(self,x,y, enemiesGroup) -> None:
        self.enemiesGroup = enemiesGroup

        self.spawnArea = Rect(x,y,500,500)
        
        self.enemySpawnRate = 100
        self.maxEnemyCount = 15

    def createEnemy(self, spawnCenterX, spawnCenterY):
        self.spawnArea.x = spawnCenterX + 500
        self.spawnArea.y = spawnCenterY - 500
        spawnPointX = random.randrange(self.spawnArea.x, self.spawnArea.x + 500)
        spawnPointY = random.randrange(self.spawnArea.y, self.spawnArea.y + 500)
        
        en = FlyingEnemy(spawnPointX, spawnPointY, True)
        self.enemiesGroup.add(en)

        # selectEnemy = random.randint(0, 1)
        # if selectEnemy == 0:
        #     en = Enemy(spawnPointX, spawnPointY, True)
        #     self.enemiesGroup.add(en)
        # elif selectEnemy == 1:
        #     en = FlyingEnemy(spawnPointX, spawnPointY, True)
        #     self.enemiesGroup.add(en)
        # elif selectEnemy == 2:
        #     en = ShooterEnemy(spawnPointX, spawnPointY, True)
        #     self.enemiesGroup.add(en)