from abc import ABC, abstractmethod


class EnemyFactory(ABC):
    @abstractmethod
    def createEnemy():
        pass