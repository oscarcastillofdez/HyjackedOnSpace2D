import random

class HardMode():
    def __init__(self) -> None:
        self.meleeEnemyDamage = 2
        self.shooterEnemyDamage = 2
        self.flyingEnemyDamage = 1
        self.barnacleEnemyDamage = 3
        self.rayEnemyDamage = 3

        self.meleeEnemyHealth = 5
        self.shoooterEnemyHealth = 3
        self.flyingEnemyHealth = 2
        self.barnacleEnemyHealth = 2

        self.playerHittedCooldown = 50

        self.enemyChaseTime = 150
        self.enemyShootCooldown = 28

        self.enemyMinChasingSpeed = 3
        self.enemyMaxChasingSpeed = 4
        self.enemyMinPatrollingSpeed = 1
        self.enemyMaxPatrollingSpeed = 2

        self.rayEnemyMinHidingTime = 50
        self.rayEnemyMaxHidingTime = 110
        self.rayEnemyMinChasingTime = 50
        self.rayEnemyMaxChasingTime = 110

        self.enemyBulletSpeed = 90

        self.flyingEnemyMaxViewDistance = 800
        self.enemyMinAttackDistance = 450

        self.playerBulletSpeed = 60
        self.playerBulletDamage = 1
        self.playerGrenadeDamage = 1
        self.playerShootGrenadeCooldown = 30
        self.playerShootCooldown = 15
        self.healthPickupHealingPower = 1

        self.maxEnemyCountOnComputerSecuence = 30
        self.countdownOnComputerScene = 90
        self.spawnDelayOnComputerScene = 55

    
    def getMeleeEnemyDamage(self):
        return self.meleeEnemyDamage
    
    def getShooterEnemyDamage(self):
        return self.shooterEnemyDamage
    
    def getFlyingEnemyDamage(self):
        return self.flyingEnemyDamage
    
    def getBarnacleEnemyDamage(self):
        return self.barnacleEnemyDamage
    
    def getRayEnemyDamage(self):
        return self.rayEnemyDamage
    
    def getMeleeEnemyHealth(self):
        return self.meleeEnemyHealth

    def getShooterEnemyHealth(self):
        return self.shoooterEnemyHealth
    
    def getFlyingEnemyHealth(self):
        return self.flyingEnemyHealth
    
    def getBarnacleEnemyHealth(self):
        return self.barnacleEnemyHealth
    
    def getEnemyChaseTime(self):
        return self.enemyChaseTime
    
    def getFlyingEnemyMaxViewDistance(self):
        return self.flyingEnemyMaxViewDistance
    
    def getEnemyMinAttackDistance(self):
        return self.enemyMinAttackDistance
    
    def getEnemyShootCooldown(self):
        return self.enemyShootCooldown
    
    def getEnemyChasingSpeed(self):
        return random.randint(self.enemyMinChasingSpeed, self.enemyMaxChasingSpeed)
    
    def getEnemyPatrollingSpeed(self):
        return random.randint(self.enemyMinPatrollingSpeed, self.enemyMaxPatrollingSpeed)
    
    def getEnemyBulletSpeed(self):
        return self.enemyBulletSpeed
    
    def getRayEnemyHidingTime(self):
        return random.randint(self.rayEnemyMinHidingTime, self.rayEnemyMaxHidingTime)
    
    def getRayEnemyChasingTime(self):
        return random.randint(self.rayEnemyMinChasingTime, self.rayEnemyMaxChasingTime)

    def getPlayerBulletDamage(self):
        return self.playerBulletDamage
    
    def getPlayerBulletSpeed(self):
        return self.playerBulletSpeed
    
    def getPlayerGrenadeDamage(self):
        return self.playerGrenadeDamage

    def getPlayerShootGrenadeCooldown(self):
        return self.playerShootGrenadeCooldown
    
    def getMaxEnemyCountOnComputerSecuence(self):
        return self.maxEnemyCountOnComputerSecuence
    
    def getPlayerShootCooldown(self):
        return self.playerShootCooldown
    
    def getHealthPickupHealingPower(self):
        return self.healthPickupHealingPower
    
    def getPlayerHittedCooldown(self):
        return self.playerHittedCooldown
    
    def getCountdownOnComputerScene(self):
        return self.countdownOnComputerScene
    
    def getSpawnDelayOnComputerScene(self):
        return self.spawnDelayOnComputerScene