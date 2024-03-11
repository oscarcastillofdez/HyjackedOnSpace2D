from Entities.Enemies.Vonreg import Vonreg
from .enemyFactory import EnemyFactory
from .flyingEnemy import FlyingEnemy
from .wallDestructible import WallDestructible
from .meleeEnemy import MeleeEnemy


class RandomEnemyFactory(EnemyFactory):
    def __init__(self, bulletsGroup, grenadesGroup, uiVonregHealthBar) -> None:
        self.bulletsGroup = bulletsGroup
        self.grenadesGroup = grenadesGroup
        self.uiVonregHealthBar = uiVonregHealthBar
    
    def createEnemy(self, columna, fila, dificulty):
        return Vonreg(columna, fila, self.grenadesGroup, dificulty, self.uiVonregHealthBar)
    
    def createEnemy2(self, columna, fila, hitBox):
        return WallDestructible(columna, fila, hitBox)
        