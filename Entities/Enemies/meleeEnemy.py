import pygame
from Constants.constants import *
from Entities.dash import Dash
from Game.collisionHandler import CollisionHandler
from .entity import Entity
from Game.spritesheet import Spritesheet
from Entities.Enemies.EnemyStates.patrol import Patrol
from Entities.Enemies.EnemyStates.chase import Chase
from Entities.Enemies.EnemyStates.attack import Attack
from Entities.Enemies.EnemyStates.die import Die

class MeleeEnemy(pygame.sprite.Sprite, Entity):
    def __init__(self,x,y, dificulty, onlyChase, lastEnemy, gunPickups):
        pygame.sprite.Sprite.__init__(self)
        # Otros objetos
        self.collisionHandler = CollisionHandler()

        # Atributos de posicion e imagen
        self.time = 0
        self.rect = pygame.Rect(0,0,100,60)
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
        
        self.damage = dificulty.getMeleeEnemyDamage()

        # Atributos de vida
        self.health = dificulty.getMeleeEnemyHealth()

        # Atributos de control de estados
        self.chaseTime = dificulty.getEnemyChaseTime()
        self.onlyChase = onlyChase

        self.lastEnemy = lastEnemy
        self.gunPickups = gunPickups

        coordinates = (0,0,24,24,4)
        scale = (100,100)
        color = (80,80,80)
        self.states = {"patrolling": Patrol(ENEMIES_PATH + 'aliens.png', self, scale, coordinates, color),
                       "chasing": Chase(ENEMIES_PATH + 'aliens.png', self, scale, coordinates, color),
                       "attacking": Attack(ENEMIES_PATH + 'aliens.png', self, scale, coordinates, color),
                       "die": Die(ENEMIES_PATH + 'aliens.png', self, scale, coordinates, color)
                       }
        
        self.state_name = "patrolling"
        if onlyChase:
            self.state_name = "chasing"
        self.current_state = self.states[self.state_name]

        self.image = self.current_state.get_initial()


    def update(self, dt, world, player,cameraOffset,enemies_group):
        if self.viewDirection > 0:
            self.current_state.left = False
        else:
            self.current_state.left = True
        
        self.time += 1
        if self.time > 6:
            self.time = 0
            self.image = self.current_state.next_sprite()

        self.current_state.update(dt, world, player, cameraOffset,enemies_group) # Llama al estado correspondiente (patrol, chase o attack)
        self.player_in_sight(world, player) # Controla la vision con el jugador
        if self.current_state.done:
            self.change_state()

    def player_in_sight(self, world, player):
        if self.viewDirection == 1:
            self.visionLine.x = self.rect.centerx
            self.visionLine.y = self.rect.y
        else:
            self.visionLine.x = self.rect.centerx - 500
            self.visionLine.y = self.rect.y

        if self.visionLine.colliderect(player.position()) and self.state_name != "attacking" and self.state_name != "die":
            self.chaseTime = 120
            self.current_state.done = True
            self.current_state.next_state = "chasing"

    def drawBullets(self, screen):
        pass
    
    def patrol(self, world, player,cameraOffset,enemies_group):
        # Calculo del movimiento
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

        if platformHitBoxList[platformCollisions[0]].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
            if self.velY >= 0 and (self.rect.bottom - platformHitBoxList[platformCollisions[0]].top) < 10: #Cayendo
                dy = platformHitBoxList[platformCollisions[0]].top - self.rect.bottom
                self.velY = 0
        
        # Actualizacion del movimiento
        self.rect.x += self.patrollingSpeed - cameraOffset[0]
        self.rect.y += dy - cameraOffset[1]
    
    def chase(self, world, player,cameraOffset,enemies_group):
        # Calculo del movimiento
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

        # Calculo de las colisiones
        tileHitBoxList = world.getTilesList()
        platformHitBoxList = world.getPlatformsList()
        destructibleHitBoxList = world.getDestructiblesList()

        tileCollisions = self.collisionHandler.checkCollisions(self, tileHitBoxList, self.moved, dy)
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

        if platformHitBoxList[platformCollisions[1]].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
            if self.velY >= 0 and (self.rect.bottom - platformHitBoxList[platformCollisions[1]].top) < 10: #Cayendo
                dy = platformHitBoxList[platformCollisions[1]].top - self.rect.bottom
                self.velY = 0

        # Actualización del movimiento
        self.rect.x -= cameraOffset[0]
        self.rect.y += dy - cameraOffset[1]
        
        self.rect.x -= self.moved

        # Comprobacion de cambio al estado atacar
        if self.rect.colliderect(player.position()):
            self.current_state.done = True
            self.current_state.next_state = "attacking"
    
    def change_state(self):
        self.state_name = self.current_state.next_state
        self.current_state.done = False
        left = self.current_state.left

        self.current_state = self.states[self.state_name]
        if left:
            self.current_state.left = True
        else:
            self.current_state.left = False
    
    def attack(self, world, player,cameraOffset,enemies_group, dt):
        player.hit(self.damage)
        self.current_state.done = True
        self.current_state.next_state = "chasing"

    def die(self,world, player,cameraOffset,enemies_group):
        if self.lastEnemy:
            grenadeLauncher = Dash(self.rect.centerx, self.rect.centery)
            self.gunPickups.add(grenadeLauncher)
            enemies_group.remove(self)
        else:
            enemies_group.remove(self)

    def hit(self, damage,deflected):
        self.health -= damage
        if self.health <= 0:
            self.state_name = "die"
            self.current_state.done = True
            self.current_state.next_state = "die"

    