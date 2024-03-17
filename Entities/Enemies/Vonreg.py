import math
from random import randint
import pygame
from Constants.constants import ENEMIES_PATH, PLAYER_PATH

from Entities.Enemies.enemy import Enemy
from Entities.grenade import Grenade
from Entities.grenadeLauncher import GrenadeLauncher
from Game.spritesheet import Spritesheet

class Vonreg(Enemy):
    def __init__(self,x,y,grenadesGroup, dificulty, healthBar, gunPickups) -> None:
        super().inheriteSprite()
        #self.image = pygame.transform.scale(pygame.image.load(ENEMIES_PATH + 'Barnacle.png'), (64,64))
        self.hitImage = pygame.image.load(ENEMIES_PATH + "hit.png")
        self.spritesheet = Spritesheet(ENEMIES_PATH + 'Vonreg/Vonreg_spritesheet.png', (200,200))
        self.spritesIdle = self.spritesheet.get_animation(0,100,100,100,8)
        self.spritesAtackMelee = self.spritesheet.get_animation(0,400,100,100,7)
        self.spritesDie = self.spritesheet.get_animation(0,800,100,100,4)

        self.image = self.spritesIdle[0]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.index = 0
        self.gunPickups = gunPickups

        self.spriteChangeCountDown = 6

        self.grenadeImage = pygame.image.load(PLAYER_PATH + "grenade.png")

        # Atributos de vision
        self.distanciaAlJugador = 100000
        self.minChasingDistance = 500
        self.minMeleeAtackDistance = 225
        self.angle = 0
        self.lineStart = (self.rect.centerx, self.rect.centery)

        # Atributos de vida
        self.maxHealth = 5
        self.currentHealth = self.maxHealth

        self.healthChangeSpeed = 5
        self.targetHealth = self.maxHealth

        self.deadDespawnCooldown = 1000

        # Atributos de interfaz
        self.observers = []
        self.healthBar = healthBar
        self.healthBar.setMaxHp(self.maxHealth)
        self.observers.append(self.healthBar)
        self.notify()

        # Atributos de control de disparo
        self.grenadesGroup = grenadesGroup
        self.meleeDamage = 1
        self.distanceDamage = 1
        self.grenadeVelocityPlatform = 8 # Velocidad de granada para alcanzar la plataforma
        self.grenadeAnglePlatform = 45 # Angulo de disparo para alcanzar la plataforma
        self.grenadeVelocitySuelo = 8 # Velocidad de granada para alcanzar el suelo
        self.grenadeAngleSuelo = 15 # Angulo de granada para disparar alcanzar el suelo
        self.selectPlaceToShoot = randint(0,1) # Selecciona aleatoriamente si disparar arriba o abajo
        self.shootGrenadeCooldownConst = 60
        self.shootCooldown = self.shootGrenadeCooldownConst

        self.states = {"patrolling": self.patrol,
                       "chasing": self.chase,
                       "attackingMelee": self.attackingMelee,
                       "attackingDistance": self.attackingDistance,
                       "die": self.die,
                       "dead": self.dead}
        
        self.current_state = "patrolling"

    def notify(self):
        for observer in self.observers:
            observer.update(self)

    def getHp(self):
        return self.currentHealth
    
    def getTargetHealth(self):
        return self.targetHealth
    
    def update(self, dt, world, player,cameraOffset, enemies_group):
        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]


        self.shootCooldown -= 5 * (dt/100)
        self.spriteChangeCountDown -= 1

        if self.spriteChangeCountDown == 0:
            self.spriteChangeCountDown = 6
            self.index += 1
            

        if self.currentHealth > self.targetHealth:
            self.currentHealth -= self.healthChangeSpeed
            self.notify()
            if self.targetHealth < 0:
                self.index = 0
                self.current_state = "die"

        self.states[self.current_state](world, player, cameraOffset, enemies_group) # Llama al estado correspondiente (patrol, chase o attack)
        self.player_in_sight(world, player)

    def patrol(self, world, player,cameraOffset,enemies_group):
        self.currentHealth = self.maxHealth
        self.targetHealth = self.maxHealth
        self.image = self.spritesIdle[0]

        if self.distanciaAlJugador < self.minChasingDistance:
            self.notify()
            self.healthBar.togleShow()
            self.current_state = "chasing"
    
    def chase(self, world, player,cameraOffset,enemies_group):
        if self.index >= len(self.spritesIdle):
            self.index = 0
        self.image = self.spritesIdle[self.index]
        if self.distanciaAlJugador >= self.minMeleeAtackDistance:
            self.index = 0
            self.current_state = "attackingDistance"
        
    def die(self,world, player,cameraOffset,enemies_group):
        if self.currentHealth <= 0:
            self.image = self.spritesDie[self.index]
            if self.index >= len(self.spritesDie) -1 :
                self.healthBar.togleShow()
                self.observers.remove(self.healthBar)

                # Al morir suelta el lanzagranadas
                grenadeLauncher = GrenadeLauncher(self.rect.centerx, self.rect.centery)
                self.gunPickups.add(grenadeLauncher)
                self.current_state = "dead"

                #enemies_group.remove(self)
    def dead(self,world, player,cameraOffset,enemies_group):
        self.deadDespawnCooldown -= 1
        if self.deadDespawnCooldown <= 0:
            enemies_group.remove(self)

    def attack():
        pass
    
    def attackingMelee(self, world, player,cameraOffset,enemies_group):
        if self.index >= len(self.spritesAtackMelee):
            self.index = 0
        self.image = self.spritesAtackMelee[self.index]
        if self.index == len(self.spritesAtackMelee) -1 :
            player.hit(self.meleeDamage)
        if self.distanciaAlJugador >= self.minMeleeAtackDistance:
            self.index = 0
            self.current_state = "attackingDistance"
    
    def attackingDistance(self, world, player,cameraOffset,enemies_group):
        if self.index >= len(self.spritesIdle):
            self.index = 0
        self.image = self.spritesIdle[self.index]
        if self.shootCooldown <= 0:
            self.shootCooldown = self.shootGrenadeCooldownConst
            self.selectPlaceToShoot = randint(0,1)
            if self.selectPlaceToShoot: # 1 -> Plataforma, 0 -> Suelo
                grenade = Grenade(self.grenadeImage, self.grenadeAnglePlatform, self.grenadeVelocityPlatform, self.rect.centerx, self.rect.y, self.distanceDamage, self, player)
                self.grenadesGroup.add(grenade)
            else:
                grenade = Grenade(self.grenadeImage, self.grenadeAngleSuelo, self.grenadeVelocitySuelo, self.rect.centerx, self.rect.y, self.distanceDamage, self, player)
                self.grenadesGroup.add(grenade)
        
        if self.distanciaAlJugador < self.minMeleeAtackDistance:
            self.index = 0
            self.current_state = "attackingMelee"
        
        if self.distanciaAlJugador > self.minChasingDistance:
            self.index = 0
            self.healthBar.togleShow()
            self.current_state = "patrolling"

    # Lógica para determinar si el jugador está dentro del rango de visión
    def player_in_sight(self, world, player):
        dx = player.position().centerx - self.rect.centerx
        dy = player.position().centery - self.rect.centery

        self.distanciaAlJugador = math.sqrt((dx**2) + (dy**2))
        self.angle = -math.degrees(math.atan2(dy, dx))

        self.lineStart = (self.rect.x, self.rect.y)

        
        
            
    def drawBullets(self,screen):
        pass
    
    def hit(self, damage,deflected):
        self.image = self.hitImage
        self.targetHealth -= damage
        
    
