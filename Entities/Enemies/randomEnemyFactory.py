from Entities.Enemies.Vonreg import Vonreg
from Entities.Enemies.rahm import Rahm
from .enemyFactory import EnemyFactory
from .flyingEnemy import FlyingEnemy
from .wallDestructible import WallDestructible
from .meleeEnemy import MeleeEnemy


class RandomEnemyFactory(EnemyFactory):
    def __init__(self, bulletsGroup, grenadesGroup, uiBossHealthBar) -> None:
        self.bulletsGroup = bulletsGroup
        self.grenadesGroup = grenadesGroup
        self.uiBossHealthBar = uiBossHealthBar
    
    def createEnemy(self, columna, fila, dificulty, gunPickups):
        return Rahm(columna, fila, self.bulletsGroup, dificulty, self.uiBossHealthBar, gunPickups)
    
    def createEnemy2(self, columna, fila, hitBox):
        return WallDestructible(columna, fila, hitBox)
        