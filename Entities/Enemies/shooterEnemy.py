import pygame
from Constants.constants import *
from Entities.bullet import Bullet
from .entity import Entity
from Game.collisionHandler import CollisionHandler
from Entities.Enemies.EnemyStates.patrol import Patrol
from Entities.Enemies.EnemyStates.chase import Chase
from Entities.Enemies.EnemyStates.attack import Attack
from Entities.Enemies.EnemyStates.die import Die
import math

class ShooterEnemy(pygame.sprite.Sprite, Entity):
    def __init__(self,x,y,dificulty, onlyChase, bullets_group):
        pygame.sprite.Sprite.__init__(self)
        # Otros objetos
        self.collisionHandler = CollisionHandler()

        # self.sprites = Spritesheet('Assets/Images/Entities/enemy trooper_walk.png',(120,120)).cargar_sprites(512,64)
        # self.image = self.sprites[0]
        # self.time = 0
        # self.index = 0
        # Atributos de posicion e imagen
        self.time = 0
        self.rect = pygame.Rect(0,0,100,100)
        self.rect.x = x
        self.rect.y = y
        
        # Atributos de movimiento
        self.moved = 0
        self.velY = 0
        self.jumpDelay = 0
        self.patrollingSpeed = dificulty.getEnemyPatrollingSpeed()
        self.chasingSpeed = dificulty.getEnemyChasingSpeed()

        # Atributos de control de vision
        self.visionLine = pygame.Rect(self.rect.centerx, self.rect.y, 500, 50) 
        self.viewDirection = 1
        self.minAtackDistance = dificulty.getEnemyMinAttackDistance() # Distancia directa hacia el jugador (diagonal)
        self.distanciaAlJugador = 0

        # Atributos de control de disparo
        self.maxShootCooldown = dificulty.getEnemyShootCooldown()
        self.shootCooldown = self.maxShootCooldown
        self.disparoImg = pygame.transform.scale(pygame.image.load('Assets/Images/Entities/Player/lazer_24.png'), (64,64))

        self.angle = 0
        self.velocidadBala = dificulty.getEnemyBulletSpeed()
        self.bulletDamage = dificulty.getShooterEnemyDamage()
        self.bullets_group = bullets_group

        # Atributos de vida
        self.health = dificulty.getShooterEnemyHealth()

        # Atributos de control de estados
        self.chaseTime = dificulty.getEnemyChaseTime()
        self.onlyChase = onlyChase

        coordinates = (0,0,64,64,6)
        scale = (100,100)
        color = (255,0,0)
        self.states = {"patrolling": Patrol(ENEMIES_PATH + 'enemyTrooperWalk.png', self, scale, coordinates, color),
                       "chasing": Chase(ENEMIES_PATH + 'enemyTrooperWalk.png', self, scale, coordinates, color),
                       "attacking": Attack(ENEMIES_PATH + 'enemyTrooperWalk.png', self, scale, coordinates, color),
                       "die": Die(ENEMIES_PATH + 'enemyTrooperWalk.png', self, scale, coordinates, color)
        }
    
        self.state_name = "patrolling"
        self.current_state = self.states[self.state_name]
        if onlyChase:
            self.state_name = "chasing"
            self.current_state = self.states[self.state_name]
        
        self.image = self.current_state.get_initial()

    def update(self, dt, world, player,cameraOffset, enemies_group):
        if self.viewDirection > 0:
            self.current_state.left = False
        else:
            self.current_state.left = True
        
        self.time += 1
        if self.time > 6:
            self.time = 0
            self.image = self.current_state.next_sprite()

        self.current_state.update(dt, world, player, cameraOffset,enemies_group)
        self.player_in_sight(world, player)
        if self.current_state.done:
            self.change_state()

    def player_in_sight(self, world, player):
        dx = player.position().centerx - self.rect.centerx
        dy = player.position().centery - self.rect.centery

        self.distanciaAlJugador = math.sqrt((dx**2) + (dy**2))
        self.angle = -math.degrees(math.atan2(dy, dx))

        if self.viewDirection == -1:
            self.visionLine.x = self.rect.centerx
            self.visionLine.y = self.rect.y
        else:
            self.visionLine.x = self.rect.centerx - 500
            self.visionLine.y = self.rect.y

        if self.visionLine.colliderect(player.position()) and self.state_name != "attacking":
            self.chaseTime = 120
            self.current_state.done = True
            self.current_state.next_state = "chasing"
    
    def patrol(self,world, player,cameraOffset,enemies_group):
        # Comportamiento cuando está patrullando
        dy = 0
        self.moved += 1
        if self.moved >= 400:
            self.viewDirection = -self.viewDirection
            self.patrollingSpeed = -self.patrollingSpeed
            self.moved = 0

        self.velY += 1
        if self.velY > 10:
             self.velY = 10
        dy += self.velY

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

        if platformHitBoxList[platformCollisions[0]].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
            if self.velY >= 0 and (self.rect.bottom - platformHitBoxList[platformCollisions[0]].top) < 10: #Cayendo
                dy = platformHitBoxList[platformCollisions[0]].top - self.rect.bottom
                self.velY = 0
        
        self.rect.x += self.patrollingSpeed - cameraOffset[0]
        self.rect.y += dy - cameraOffset[1]
    
    def chase(self,world, player,cameraOffset,enemies_group):
        self.jumpDelay -= 1
        self.chaseTime -= 1

        if self.chaseTime <= 0 and not self.onlyChase:
            self.current_state.done = True
            self.current_state.next_state = "patrolling"
            
        dy = 0
        self.moved = 0


        if player.position().x > self.rect.x:
            self.viewDirection = 1
            self.moved -= self.chasingSpeed

        if player.position().x < self.rect.x:
            self.viewDirection = -1
            self.moved += self.chasingSpeed

        self.velY += 1
        if self.velY > 10:
            self.velY = 1
        
        dy += self.velY

        tileHitBoxList = world.getTilesList()
        platformHitBoxList = world.getPlatformsList()
        destructibleHitBoxList = world.getDestructiblesList()

        tileCollisions = self.collisionHandler.checkCollisions(self, tileHitBoxList, self.patrollingSpeed, dy)
        platformCollisions = self.collisionHandler.checkCollisions(self, platformHitBoxList, self.patrollingSpeed, dy)
        destructibleCollisions = self.collisionHandler.checkCollisions(self, destructibleHitBoxList, self.patrollingSpeed, dy)

        if tileCollisions[0] >= 0 or destructibleCollisions[0] >= 0:
            if self.jumpDelay <= 0:
                self.jumpDelay = 50
                self.velY = -12
                dy = self.velY

            self.moved = 0

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

        if platformHitBoxList[platformCollisions[0]].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
            if self.velY >= 0 and (self.rect.bottom - platformHitBoxList[platformCollisions[0]].top) < 10: #Cayendo
                dy = platformHitBoxList[platformCollisions[0]].top - self.rect.bottom
                self.velY = 0

        self.rect.x -= cameraOffset[0]
        self.rect.y += dy - cameraOffset[1]
        
        self.rect.x -= self.moved

        if self.distanciaAlJugador < self.minAtackDistance:
            self.current_state.done = True
            self.current_state.next_state = "attacking"
    
    def attack(self,world, player,cameraOffset,enemies_group, dt):
        # Disparar cada x segundos
        dy = 0

        self.velY += 1
        if self.velY > 10:
            self.velY = 1
        
        dy += self.velY

        self.shootCooldown -= 10 * (dt/100)
        if self.shootCooldown <= 0:
            self.shootCooldown = self.maxShootCooldown
            disparo = Bullet(self.disparoImg, self.angle, self.bulletDamage, self.velocidadBala, self.rect.x, self.rect.y, self, player, False)
            self.bullets_group.add(disparo)

        tileHitBoxList = world.getTilesList()
        tileCollisions = self.collisionHandler.checkCollisions(self, tileHitBoxList, 0, dy)

        if tileCollisions[1] >= 0:
            if self.velY < 0: #Saltando
                dy = tileHitBoxList[tileCollisions[1]].bottom - self.rect.top
                self.velY = 0
            elif self.velY >= 0: #Cayendo
                dy = tileHitBoxList[tileCollisions[1]].top - self.rect.bottom
                self.velY = 0

        self.rect.x -= cameraOffset[0]
        self.rect.y += dy - cameraOffset[1]

        if self.distanciaAlJugador > self.minAtackDistance:
            self.current_state.done = True
            self.current_state.next_state = "chasing"
    
    def change_state(self):
        self.state_name = self.current_state.next_state
        self.current_state.done = False
        left = self.current_state.left

        self.current_state = self.states[self.state_name]
        if left:
            self.current_state.left = True
        else:
            self.current_state.left = False
    
    def drawBullets(self, screen):
        pass

    def die(self,world, player,cameraOffset,enemies_group):
        enemies_group.remove(self)

    def hit(self, damage,deflected):
        self.health -= damage
        if self.health <= 0:
            self.current_state.done = True
            self.current_state.next_state = "die"  