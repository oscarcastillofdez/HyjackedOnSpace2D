from Entities.Enemies.Vonreg import Vonreg
from Entities.Enemies.barnacleEnemy import BarnacleEnemy
from Entities.Enemies.rahm import Rahm
from Entities.Enemies.rayEnemy import RayEnemy
from Entities.Enemies.shooterEnemy import ShooterEnemy
from .enemyFactory import EnemyFactory
from .flyingEnemy import FlyingEnemy
from .wallDestructible import WallDestructible
from .meleeEnemy import MeleeEnemy


class SelectedEnemyFactory(EnemyFactory):
    def __init__(self, bulletsGroup, grenadesGroup, uiBossHealthBar, uiCroshair, dificulty, gunPickups) -> None:
        self.bulletsGroup = bulletsGroup
        self.grenadesGroup = grenadesGroup
        self.uiBossHealthBar = uiBossHealthBar
        self.uiCroshair = uiCroshair
        self.dificulty = dificulty
        self.gunPickups = gunPickups    
    
    def createRahm(self, columna, fila):
        return Rahm(columna, fila, self.bulletsGroup, self.dificulty, self.uiBossHealthBar, self.gunPickups, self.uiCroshair)
    
    def createVonreg(self, columna, fila):
        return Vonreg(columna, fila, self.grenadesGroup, self.dificulty, self.uiBossHealthBar, self.gunPickups)
    
    def createRay(self, columna, fila):
        return RayEnemy(columna, fila,self.dificulty)
    
    def createBarnacle(self, columna, fila):
        return BarnacleEnemy(columna, fila,self.dificulty)
    
    def createFlying(self, columna, fila):
        return FlyingEnemy(columna, fila,self.dificulty, False, self.bulletsGroup)
    
    def createShooter(self, columna, fila):
        return ShooterEnemy(columna, fila,self.dificulty, False, self.bulletsGroup)
    
    def createMelee(self, columna, fila):
        return MeleeEnemy(columna, fila,self.dificulty, False)

    def createBox(self, columna, fila,destructibleTile_list):
        return WallDestructible(columna, fila,destructibleTile_list)