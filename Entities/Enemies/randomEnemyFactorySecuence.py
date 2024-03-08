from pygame import Rect

from Entities.Enemies.barnacleEnemy import BarnacleEnemy
from Entities.Enemies.rayEnemy import RayEnemy
from Entities.Enemies.shooterEnemy import ShooterEnemy

from .enemyFactory import EnemyFactory
from .flyingEnemy import FlyingEnemy
from .wallDestructible import WallDestructible
from .meleeEnemy import MeleeEnemy
import random
from Constants.constants import *

class RandomEnemyFactorySecuence(EnemyFactory):
    def __init__(self,enemiesGroup, dificulty) -> None:
        self.enemiesGroup = enemiesGroup
        self.dificulty = dificulty

        self.spawnArea = Rect(0,0,500,500)
        
        self.enemySpawnRate = 100
        self.maxEnemyCount = 15

    def createEnemy(self, spawnCenterX, spawnCenterY):
        self.spawnArea.x = spawnCenterX + 500
        self.spawnArea.y = spawnCenterY - 500
        spawnPointX = random.randrange(self.spawnArea.x, self.spawnArea.x + 500)
        spawnPointY = random.randrange(self.spawnArea.y, self.spawnArea.y + 500)
        
        selectEnemy = random.randint(0, 3)
        if selectEnemy == 0:
            en = ShooterEnemy(spawnPointX, spawnPointY, self.dificulty, True)
            self.enemiesGroup.add(en)
        elif selectEnemy == 1:
            en = ShooterEnemy(spawnPointX, spawnPointY, self.dificulty, True)
            self.enemiesGroup.add(en)
        elif selectEnemy == 2:
            en = ShooterEnemy(spawnPointX, spawnPointY, self.dificulty, True)
            self.enemiesGroup.add(en)
        elif selectEnemy == 3:
            en = ShooterEnemy(spawnPointX, spawnPointY, self.dificulty, True)
            self.enemiesGroup.add(en)