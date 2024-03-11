import math
from random import randint
import pygame
from Constants.constants import ENEMIES_PATH

from Entities.Enemies.entity import Entity
from Entities.bullet import Bullet

class Rahm(pygame.sprite.Sprite, Entity):
    def __init__(self,x,y,bulletsGroup, dificulty, healthBar, gunPickups) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(ENEMIES_PATH + 'Barnacle.png'), (64,64))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Atributos de vision
        self.distanciaAlJugador = 1000
        self.angle = 0
        self.lineStart = (self.rect.centerx, self.rect.centery)

        # Atributos de movimiento
        self.teleportCooldown = randint(60, 120)
        self.selectTeleportZone = randint(0,2)
        self.upperZoneX = 74 * 32
        self.upperZoneY = 59 * 32
        self.middleZoneX = 64 * 32
        self.middleZoneY = 68 * 32
        self.lowerZoneX = 57 * 32
        self.lowerZoneY = 78 * 32

        # Atributos de daño
        self.bulletsGroup = bulletsGroup
        self.attackCooldown = randint(60, 120)
        self.damage = 3
        self.shootCooldown = 4
        self.shotsCount = 0
        self.bulletImage =  pygame.transform.scale(pygame.image.load(ENEMIES_PATH + '/Rahm/rahm_bullet.png'), (32,32))
        self.bulletSpeed = 50

        self.states = {"patrolling": self.patrol,
                       "chasing": self.chase,
                       "attacking": self.attack,
                       "die": self.die}
        
        self.current_state = "patrolling"
    
    def update(self, dt, world, player,cameraOffset, enemies_group):
        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]

        self.attackCooldown -= 1
        if self.attackCooldown < 0:
            self.attackCooldown = randint(60, 120)
            self.current_state = "chasing"

        self.player_in_sight(world, player)
        self.states[self.current_state](world, player, cameraOffset, enemies_group) # Llama al estado correspondiente (patrol, chase o attack)

    def patrol(self, world, player,cameraOffset,enemies_group):
        if self.distanciaAlJugador < 1000:
            self.current_state = "chasing"
    
    def chase(self, world, player,cameraOffset,enemies_group):
        self.attackCooldown -= 1
        if self.attackCooldown < 0:
            self.attackCooldown = randint(60, 120)
            self.current_state = "attacking"
            
        self.shootCooldown -= 1
        if self.shootCooldown <= 0:
            self.shootCooldown = 4

    def die(self,world, player,cameraOffset,enemies_group):
        pass
    
    def attack(self, world, player,cameraOffset,enemies_group):
        if self.shotsCount < 3:
            self.shootCooldown -= 1
            if self.shootCooldown <= 0:
                self.shootCooldown = 4
                disparo = Bullet(self.bulletImage, self.angle, self.damage, self.bulletSpeed, self.rect.x, self.rect.y, self, player)
                self.bulletsGroup.add(disparo)
        else: 
            self.shotsCount = 0
            self.current_state = "chasing"
    
    def drawBullets(self,screen):
        pass
    
    def kill(self):
        pass 
    
    def player_in_sight(self, world, player):
        dx = player.position().centerx - self.rect.centerx
        dy = player.position().centery - self.rect.centery

        self.distanciaAlJugador = math.sqrt((dx**2) + (dy**2))
        self.angle = -math.degrees(math.atan2(dy, dx))

        self.lineStart = (self.rect.x, self.rect.y)


    
