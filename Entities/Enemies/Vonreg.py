import math
from random import randint
import pygame
from Constants.constants import ENEMIES_PATH, PLAYER_PATH

from Entities.Enemies.entity import Entity
from Entities.grenade import Grenade
from UI.uiVonregHealthBar import UIVonregHealthBar

class Vonreg(pygame.sprite.Sprite, Entity):
    def __init__(self,x,y,grenadesGroup, dificulty, healthBar) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(ENEMIES_PATH + 'Barnacle.png'), (64,64))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.grenadeImage = pygame.image.load(PLAYER_PATH + "grenade.png")

        # Atributos de vision
        self.distanciaAlJugador = 0
        self.minMeleeAtackDistance = 50
        self.angle = 0
        self.lineStart = (self.rect.centerx, self.rect.centery)

        # Atributos de vida
        self.maxHealth = 300
        self.currentHealth = self.maxHealth


        self.healthChangeSpeed = 5
        self.targetHealth = self.maxHealth

        # Atributos de interfaz
        self.observers = []
        self.healthBar = healthBar
        self.observers.append(self.healthBar)
        self.notify()

        # Atributos de control de disparo
        self.grenadesGroup = grenadesGroup
        self.meleeDamage = 1
        self.distanceDamage = 1
        self.grenadeVelocityPlatform = 9 # Velocidad de granada para alcanzar la plataforma
        self.grenadeAnglePlatform = 65 # Angulo de disparo para alcanzar la plataforma
        self.grenadeVelocitySuelo = 8 # Velocidad de granada para alcanzar el suelo
        self.grenadeAngleSuelo = 45 # Angulo de granada para disparar alcanzar el suelo
        self.selectPlaceToShoot = randint(0,1) # Selecciona aleatoriamente si disparar arriba o abajo
        self.shootGrenadeCooldownConst = 60
        self.shootCooldown = self.shootGrenadeCooldownConst

        self.states = {"patrolling": self.patrol,
                       "chasing": self.chase,
                       "attackingMelee": self.attackingMelee,
                       "attackingDistance": self.attackingDistance,
                       "die": self.die}
        self.current_state = "chasing"

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

        self.shootCooldown -= 1

        if self.currentHealth > self.targetHealth:
            self.currentHealth -= self.healthChangeSpeed
            self.notify()
            if self.targetHealth < 0:
                self.current_state = "die"

        self.states[self.current_state](world, player, cameraOffset, enemies_group) # Llama al estado correspondiente (patrol, chase o attack)
        self.player_in_sight(world, player)

    def patrol(self, world, player,cameraOffset,enemies_group):
        pass
    
    def chase(self, world, player,cameraOffset,enemies_group):
        pass

    def die(self,world, player,cameraOffset,enemies_group):
        if self.currentHealth <= 0:
            self.healthBar.togleShow()
            self.observers.remove(self.healthBar)
            enemies_group.remove(self)
    
    def attackingMelee(self, world, player,cameraOffset,enemies_group):
        player.hit(self.meleeDamage)
    
    def attackingDistance(self, world, player,cameraOffset,enemies_group):
        
        if self.shootCooldown <= 0:
            self.shootCooldown = self.shootGrenadeCooldownConst
            self.selectPlaceToShoot = randint(0,1)
            if self.selectPlaceToShoot: # 1 -> Plataforma, 0 -> Suelo
                grenade = Grenade(self.grenadeImage, self.grenadeAnglePlatform, self.grenadeVelocityPlatform, self.rect.x, self.rect.y, self.distanceDamage, self, player)
                self.grenadesGroup.add(grenade)
            else:
                grenade = Grenade(self.grenadeImage, self.grenadeAngleSuelo, self.grenadeVelocitySuelo, self.rect.x, self.rect.y, self.distanceDamage, self, player)
                self.grenadesGroup.add(grenade)

    # Lógica para determinar si el jugador está dentro del rango de visión
    def player_in_sight(self, world, player):
        dx = player.position().centerx - self.rect.centerx
        dy = player.position().centery - self.rect.centery

        self.distanciaAlJugador = math.sqrt((dx**2) + (dy**2))
        self.angle = -math.degrees(math.atan2(dy, dx))

        self.lineStart = (self.rect.x, self.rect.y)
        
        if self.distanciaAlJugador < self.minMeleeAtackDistance:
            self.current_state = "attackingMelee"
        else:
            self.current_state = "attackingDistance"
            
    def drawBullets(self,screen):
        pass
    
    def hit(self, damage):
        self.targetHealth -= damage
        print(self.currentHealth)
        
    
