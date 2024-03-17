import random

class EasyMode():
    def __init__(self) -> None:
        self.meleeEnemyDamage = 1
        self.shooterEnemyDamage = 1
        self.flyingEnemyDamage = 1
        self.barnacleEnemyDamage = 3
        self.rayEnemyDamage = 1

        self.meleeEnemyHealth = 3
        self.shoooterEnemyHealth = 2
        self.flyingEnemyHealth = 2
        self.barnacleEnemyHealth = 1

        self.playerHittedCooldown = 65

        self.enemyChaseTime = 100
        self.enemyShootCooldown = 100

        self.enemyMinChasingSpeed = 3
        self.enemyMaxChasingSpeed = 3
        self.enemyMinPatrollingSpeed = 1
        self.enemyMaxPatrollingSpeed = 1

        self.rayEnemyMinHidingTime = 90
        self.rayEnemyMaxHidingTime = 140
        self.rayEnemyMinChasingTime = 60
        self.rayEnemyMaxChasingTime = 120

        self.enemyBulletSpeed = 80

        self.flyingEnemyMaxViewDistance = 400
        self.enemyMinAttackDistance = 300

        self.playerBulletSpeed = 80
        self.playerBulletDamage = 1
        self.playerGrenadeDamage = 3
        self.playerShootGrenadeCooldown = 25
        self.playerShootCooldown = 12
        self.healthPickupHealingPower = 3

        self.maxEnemyCountOnComputerSecuence = 20
        self.countdownOnComputerScene = 30
        self.spawnDelayOnComputerScene = 60

    
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