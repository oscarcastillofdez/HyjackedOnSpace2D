from Enemies.enemyFactory import EnemyFactory
from Enemies.flyingEnemy import FlyingEnemy
from Enemies.enemy import Enemy

class RandomEnemyFactory(EnemyFactory):
    def __init__(self) -> None:
        pass
    
    def createEnemy(self, columna, fila, gv):
        return FlyingEnemy(columna, fila, gv)