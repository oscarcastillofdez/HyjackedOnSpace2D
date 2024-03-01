from .enemyFactory import EnemyFactory
from .flyingEnemy import FlyingEnemy
from .enemy import Enemy

class RandomEnemyFactory(EnemyFactory):
    def __init__(self) -> None:
        pass
    
    def createEnemy(self, columna, fila, gv):
        return FlyingEnemy(columna, fila, gv)