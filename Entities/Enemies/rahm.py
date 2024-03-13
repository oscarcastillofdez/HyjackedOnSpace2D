import math
from random import randint
import pygame
from Constants.constants import ENEMIES_PATH

from Entities.Enemies.entity import Entity
from Entities.bullet import Bullet
from Game.collisionHandler import CollisionHandler
from Game.spritesheet import Spritesheet

class Rahm(pygame.sprite.Sprite, Entity):
    def __init__(self,x,y,bulletsGroup, dificulty, healthBar, gunPickups, uiCroshair) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.collisionHandler = CollisionHandler()
        self.spritesheetRunning = Spritesheet(ENEMIES_PATH + '/Rahm/rahm_running.png', (128,128))
        self.spritesheetShooting = Spritesheet(ENEMIES_PATH + '/Rahm/rahm_range_attack.png', (128,128))
        self.spritesheetMelee = Spritesheet(ENEMIES_PATH + '/Rahm/rahm_melee_attack.png', (128,128))

        self.spritesRunning = self.spritesheetRunning.get_animation(0,0,128,128,8)
        self.spritesShooting = self.spritesheetShooting.get_animation(0,0,128,128,7)
        self.spritesMelee = self.spritesheetMelee.get_animation(0,0,128,128,9)

        self.image = self.spritesRunning[0]
        self.index = 0
        self.spriteChangeCountDown = 2

        self.rect = self.image.get_rect()
        self.rect.x = 64 * 32
        self.rect.y = 68 * 32
        self.playerPosition = pygame.Rect(0,0,0,0)
        self.globalOffset = (0,0)


        # Atributos de vision
        self.distanciaAlJugador = 1000
        self.angle = 0

        # Atributos de movimiento
        self.numTeleportZones = 2
        self.currentZone = 1
        self.upperZoneX = 74 * 32
        self.upperZoneY = 57 * 32
        self.middleZoneX = 64 * 32
        self.middleZoneY = 68 * 32
        self.lowerZoneX = 57 * 32
        self.lowerZoneY = 78 * 32
        self.offsetX = 0
        self.offsetY = 0
        self.stunnedCooldownMax = 200
        self.stunnedCooldown = self.stunnedCooldownMax
        self.moved = 0
        self.viewDirection = 0
        self.patrollingSpeed = 5
        self.velY = 0

        # Atributos de vida
        self.maxHealth = 15
        self.targetHealth = self.maxHealth
        self.currentHealth = self.maxHealth
        self.healthChangeSpeed = 1

        # Atributos de daño
        self.bulletsGroup = bulletsGroup
        self.attackCooldown = randint(220, 300)
        self.damage = 1.01
        self.shootCooldown = 2
        self.maxShotsCount = 3
        self.shotsCount = 0
        self.bulletImage =  pygame.transform.scale(pygame.image.load(ENEMIES_PATH + '/Rahm/rahm_bullet.png'), (50,35))
        self.bulletSpeed = 35

        # Atributos de interfaz
        self.uiCroshair = uiCroshair
        self.healthBar = healthBar
        self.observers = []
        self.observers.append(self.uiCroshair)
        self.observers.append(self.healthBar)
        self.healthBar.setMaxHp(self.maxHealth)


        self.states = {"patrolling": self.patrol,
                       "chasing": self.chase,
                       "attacking": self.attack,
                       "attackingMelee": self.attackMelee,
                       "die": self.die,
                       "dead": self.dead,
                       "stunned": self.stunned}
        
        self.current_state = "patrolling"

    def getPlayerPosition(self):
        return self.playerPosition
    
    def getHp(self):
        return self.currentHealth
    
    def getTargetHealth(self):
        return self.targetHealth
    
    def notify(self,player):
        for observer in self.observers:
            self.playerPosition = player.position()
            observer.update(self)
    

    def update(self, dt, world, player,cameraOffset, enemies_group):
        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]

        self.offsetX -= cameraOffset[0]
        self.offsetY -= cameraOffset[1]

        self.spriteChangeCountDown -= 1

        if self.spriteChangeCountDown == 0:
            self.spriteChangeCountDown = 2
            self.index += 1

        if self.currentHealth > self.targetHealth:
            self.currentHealth -= self.healthChangeSpeed
            self.notify(player)
            if self.targetHealth < 0:
                self.index = 0
                if self.current_state != "dead":
                    self.current_state = "die"
        
        self.globalOffset = world.getGlobalOffset()
            
        self.player_in_sight(world, player)
        self.states[self.current_state](world, player, cameraOffset, enemies_group) # Llama al estado correspondiente (patrol, chase o attack)

    def patrol(self, world, player,cameraOffset,enemies_group):
        if self.distanciaAlJugador < 1000:
            self.healthBar.togleShow()
            self.index = 0
            self.current_state = "chasing"

    def move(self, world):
        if self.index >= len(self.spritesRunning):
            self.index = 0
        self.image = self.spritesRunning[self.index]
        
        dy = 0

        self.moved += 1
        if self.moved >= 150:
            self.viewDirection = -self.viewDirection
            self.patrollingSpeed = -self.patrollingSpeed
            self.moved = 0

        self.velY += 1
        if self.velY > 10:
             self.velY = 10
        dy += self.velY

        # Calculo de las colisiones
        tileHitBoxList = world.getTilesList()
        platformHitBoxList = world.getPlatformsList()
        destructibleHitBoxList = world.getDestructiblesList()

        tileCollisions = self.collisionHandler.checkCollisions(self, tileHitBoxList, self.patrollingSpeed, dy)
        platformCollisions = self.collisionHandler.checkCollisions(self, platformHitBoxList, self.patrollingSpeed, dy)
        destructibleCollisions = self.collisionHandler.checkCollisions(self, destructibleHitBoxList, self.patrollingSpeed, dy)

        if tileCollisions[0] >= 0 or destructibleCollisions[0] >= 0:
            self.patrollingSpeed = -self.patrollingSpeed
            self.viewDirection = -self.viewDirection

        if tileCollisions[1] >= 0:
            if self.velY < 0: #Saltando
                dy = tileHitBoxList[tileCollisions[1]].bottom - self.rect.top
                self.velY = 0
            elif self.velY >= 0: #Cayendo
                dy = tileHitBoxList[tileCollisions[1]].top - self.rect.bottom
                self.velY = 0

        if destructibleCollisions[1] >= 0:
            if self.velY < 0: #Saltando
                dy = destructibleHitBoxList[destructibleCollisions[1]].bottom - self.rect.top
                self.velY = 0
            elif self.velY >= 0: #Cayendo
                dy = destructibleHitBoxList[destructibleCollisions[1]].top - self.rect.bottom
                self.velY = 0

        if platformHitBoxList[platformCollisions[1]].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
            if self.velY >= 0 and (self.rect.bottom - platformHitBoxList[platformCollisions[1]].top) < 10: #Cayendo
                dy = platformHitBoxList[platformCollisions[1]].top - self.rect.bottom
                self.velY = 0
        
        # Actualizacion del movimiento
        self.rect.x += self.patrollingSpeed
        self.rect.y += dy
    
    def chase(self, world, player,cameraOffset,enemies_group):
        self.move(world)
        
        self.attackCooldown -= 1
        
        if self.attackCooldown <= 0:
            self.uiCroshair.togleShow(False)
            self.notify(player)
            self.index = 0
            self.current_state = "attacking"
        elif self.attackCooldown < 60:
            self.uiCroshair.togleShow(True)
            self.notify(player)
        
        if self.distanciaAlJugador < 75:
            self.index = 0
            self.current_state = "attackingMelee"

    def dead(self,world, player,cameraOffset,enemies_group):
        enemies_group.remove(self)

    
    def die(self,world, player,cameraOffset,enemies_group):
        if self.currentHealth <= 0:
            self.index = 0
            self.current_state = "dead"
            self.healthBar.togleShow()
            self.observers.remove(self.healthBar)
            self.observers.remove(self.uiCroshair)

    def attackMelee(self, world, player,cameraOffset,enemies_group):
        if self.index >= len(self.spritesMelee):
            self.index = 0
        self.image = self.spritesMelee[self.index]
        if self.index == 4:
            player.hit(math.floor(self.damage))

        if self.distanciaAlJugador >= 75:
            self.index = 0
            self.current_state = "chasing"

        
    def attack(self, world, player,cameraOffset,enemies_group):
        self.image = self.spritesShooting[3]
        if self.index >= 3:
            self.index = 3
        self.image = self.spritesShooting[self.index]
        

        if self.shotsCount < self.maxShotsCount:
            self.shootCooldown -= 1
            if self.shootCooldown <= 0:
                self.shotsCount += 1
                self.shootCooldown = 4
                disparo = Bullet(self.bulletImage, self.angle, math.floor(self.damage), self.bulletSpeed, self.rect.x + 60, self.rect.y, self, player, False)
                self.bulletsGroup.add(disparo)
        else: 
            self.shotsCount = 0
            self.attackCooldown = randint(220, 300)
            self.index = 0
            self.current_state = "chasing"
    
    def drawBullets(self,screen):
        pass
    
    def teleport(self):
        selectTeleportZone = randint(0,self.numTeleportZones)
        
        while selectTeleportZone == self.currentZone:
            selectTeleportZone = randint(0,self.numTeleportZones)
    
        if selectTeleportZone == 0:
            self.rect.x = self.upperZoneX + self.offsetX
            self.rect.y = self.upperZoneY + self.offsetY 
            self.currentZone = 0
        if selectTeleportZone == 1:
            self.rect.x = self.middleZoneX + self.offsetX
            self.rect.y = self.middleZoneY + self.offsetY
            self.currentZone = 1
        if selectTeleportZone == 2:
            self.rect.x = self.lowerZoneX + self.offsetX
            self.rect.y = self.lowerZoneY + self.offsetY
            self.currentZone = 2
    
    def stunned(self,world, player,cameraOffset,enemies_group):
        self.stunnedCooldown -= 1
        if self.stunnedCooldown < 0:
            self.shotsCount = 0
            self.attackCooldown = randint(220, 300)
            self.index = 0
            self.current_state = "chasing"
        
    def hit(self, damage, deflected):
        # Arreglo sencillo y chafulleiro para no tener que pasar nuevos parametros a hit
        # Si el daño recibido es el mismo que el daño de rahm, entonces la bala fue deflected por el escudo: 
            #Rahm es aturdido daño
        # Si el daño recibido es distinto, entonces la bala la disparo directamente el jugador: 
            # Si Rahm no esta aturdido se teletransporta a una nueva ubicacion
            # Si Rahm esta aturdido, recibe daño
        
        if deflected:
            self.stunnedCooldown = self.stunnedCooldownMax 
            self.index = 0
            self.current_state = "stunned"
        else:
            if self.current_state == "stunned":
                self.targetHealth -= damage
            else:
                self.teleport()
            
    
    def player_in_sight(self, world, player):
        dx = player.position().centerx - self.rect.centerx
        dy = player.position().centery - self.rect.centery

        self.distanciaAlJugador = math.sqrt((dx**2) + (dy**2)) # Calculo de la hipotenusa
        self.angle = -math.degrees(math.atan2(dy, dx))

    
