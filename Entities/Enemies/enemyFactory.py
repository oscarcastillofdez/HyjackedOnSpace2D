from abc import ABC, abstractmethod


class EnemyFactory(ABC):
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def createEnemy():
        pass