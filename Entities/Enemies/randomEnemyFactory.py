from .enemyFactory import EnemyFactory
from .flyingEnemy import FlyingEnemy
from .wallDestructible import WallDestructible
from .meleeEnemy import MeleeEnemy


class RandomEnemyFactory(EnemyFactory):
    def __init__(self) -> None:
        pass
    
    def createEnemy(self, columna, fila, dificulty):
        return FlyingEnemy(columna, fila, dificulty, False)
    
    def createFlyingEnemy(self, columna, fila, dificulty):
        return FlyingEnemy(columna, fila, dificulty, False)
    
    def createEnemy2(self, columna, fila, hitBox):
        return WallDestructible(columna, fila, hitBox)
        