import random

class EasyMode():
    def __init__(self) -> None:
        self.meleeEnemyDamage = 1
        self.shooterEnemyDamage = 1
        self.flyingEnemyDamage = 1
        self.barnacleEnemyDamage = 2
        self.rayEnemyDamage = 1

        self.meleeEnemyHealth = 1
        self.shoooterEnemyHealth = 1
        self.flyingEnemyHealth = 1
        self.barnacleEnemyHealth = 1

        self.enemyChaseTime = 120
        self.enemyShootCooldown = 30

        self.enemyMinChasingSpeed = 2
        self.enemyMaxChasingSpeed = 4
        self.enemyMinPatrollingSpeed = 1
        self.enemyMaxPatrollingSpeed = 1

        self.rayEnemyMinHidingTime = 60
        self.rayEnemyMaxHidingTime = 120
        self.rayEnemyMinChasingTime = 60
        self.rayEnemyMaxChasingTime = 120

        self.enemyBulletSpeed = 10

        self.flyingEnemyMaxViewDistance = 600
        self.enemyMinAttackDistance = 300

        self.playerBulletSpeed = 10
        self.playerBulletDamage = 1
        self.playerGrenadeDamage = 1
        self.playerShootCooldown = 15
        self.healthPickupHealingPower = 3

        self.maxEnemyCountOnComputerSecuence = 15
    
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
    
    def getMaxEnemyCountOnComputerSecuence(self):
        return self.getMaxEnemyCountOnComputerSecuence
    
    def getPlayerShootCooldown(self):
        return self.playerShootCooldown
    
    def getHealthPickupHealingPower(self):
        return self.healthPickupHealingPower