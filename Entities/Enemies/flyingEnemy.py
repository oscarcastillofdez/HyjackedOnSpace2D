import pygame

from Game.collisionHandler import CollisionHandler
from .entity import Entity
import math
from Entities.Enemies.EnemyStates.patrol import Patrol
from Entities.Enemies.EnemyStates.chase import Chase
from Entities.Enemies.EnemyStates.attack import Attack
from Entities.Enemies.EnemyStates.die import Die

from Game.spritesheet import Spritesheet
from Constants.constants import *
from Entities.bullet import Bullet


class FlyingEnemy(pygame.sprite.Sprite, Entity):
    def __init__(self,x,y, dificulty, onlyChase, bullets_group) -> None:
        pygame.sprite.Sprite.__init__(self)
        # Otros objetos
        self.collisionHandler = CollisionHandler()
        
        # Atributos de posicion e imagen
        #self.sprites = Spritesheet('Assets/Images/Entities/32bitsspritesheet.png',(120,120)).get_animation(0,0,223,223,30)
        self.hitImage = pygame.image.load(ENEMIES_PATH + "hit.png")
        self.index = 0
        self.time = 0
        self.rect = pygame.Rect(0,0,120,120)
        self.rect.x = x
        self.rect.y = y - 100

        # Atributos de movimiento
        self.moved = 0
        self.patrollingSpeed = dificulty.getEnemyPatrollingSpeed()
        self.chasingSpeed = dificulty.getEnemyChasingSpeed()
        self.velY = 0
        
        # Atributos de control de vision
        self.viewDirection = 1
        self.maxViewDistance = dificulty.getFlyingEnemyMaxViewDistance() # Distancia directa hacia el jugador (diagonal)
        self.minAtackDistance = dificulty.getEnemyMinAttackDistance() # Distancia directa hacia el jugador (diagonal)
        self.distanciaAlJugador = 0
        self.angle = 0
        self.lineStart = (self.rect.centerx, self.rect.centery)

        # Atributos de control de disparo
        self.disparoImg = pygame.transform.scale(pygame.image.load('Assets/Images/Entities/Player/lazer_24.png'), (64,64))
        self.maxShootCooldown = dificulty.getEnemyShootCooldown()
        self.shootCooldown = self.maxShootCooldown
        self.velocidadBala = dificulty.getEnemyBulletSpeed()
        self.bulletDamage = dificulty.getFlyingEnemyDamage()
        self.bullets_group = bullets_group

        # Atributos de vida
        self.health = dificulty.getFlyingEnemyHealth()

        # Atributos de control de estados
        self.onlyChase = onlyChase
        self.chaseTime = dificulty.getEnemyChaseTime()

        scale = (120,120)
        color = (80,80,80)
        self.states = {"patrolling": Patrol(FLYING_ENEMY_PATH, self, scale, (96,96,48,48,2), color),
                       "chasing": Chase(FLYING_ENEMY_PATH, self, scale, (96,96,48,48,2), color),
                       "attacking": Attack(FLYING_ENEMY_PATH, self, scale, (0,96,48,48,2), color),
                       "die": Die(FLYING_ENEMY_PATH, self, scale, (0,0,24,24,4),color)}

        # self.states = {"patrolling": self.patrol,
        #                "chasing": self.chase,
        #                "attacking": self.attack,
        #                "die": self.die}
        
        self.state_name = "patrolling"
        self.current_state = self.states["patrolling"]

        if onlyChase:
            self.state_name = "chasing"
            self.current_state = self.states["chasing"]
        
        self.image = self.current_state.get_initial()
                
    def update(self, dt, world, player, cameraOffset,enemies_group):
        if self.viewDirection > 0:
            self.current_state.left = False
        else:
            self.current_state.left = True
        self.time += 1
        if self.time > 6:
            self.time = 0
            self.index += 1
            #if self.index >= len(self.sprites):
                #self.index=0
            self.image = self.current_state.next_sprite()

        self.states[self.state_name].update(dt, world, player, cameraOffset,enemies_group)
        self.player_in_sight(world, player)
        if self.current_state.done:
            self.change_state()

    def patrol(self, world, player, cameraOffset,enemies_group):
        # Comportamiento cuando está patrullando
        dy = 0

        self.moved += 1
        if self.moved >= 400:
            self.viewDirection = -self.viewDirection
            self.patrollingSpeed = -self.patrollingSpeed
            self.moved = 0
        
        # Se calculan las colisiones en ambos ejes
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

    
    def chase(self, world, player,cameraOffset,enemies_group):
        self.chaseTime -= 1

        if self.chaseTime <= 0 and not self.onlyChase:
            self.current_state.next_state = "patrolling"
            self.current_state.done = True
            
        self.moved = 0

        if player.position().x > self.rect.x:
            self.viewDirection = 1
            self.moved -= self.chasingSpeed

        if player.position().x < self.rect.x:
            self.viewDirection = -1
            self.moved += self.chasingSpeed

        tileHitBoxList = world.getTilesList()
        destructibleHitBoxList = world.getDestructiblesList()

        auxRect = pygame.Rect(self.rect.x - self.moved, self.rect.y, self.rect.width, self.rect.height)
        
        tileIndex = auxRect.collidelist(tileHitBoxList)

        destructibleIndex = auxRect.collidelist(destructibleHitBoxList)
        
        if tileIndex >= 0 or destructibleIndex >= 0:
            self.moved = 0

        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]
        
        self.rect.x -= self.moved

        if self.distanciaAlJugador < self.minAtackDistance:
            self.current_state.next_state = "attacking"
            self.current_state.done = True
    
    def attack(self, world, player,cameraOffset,enemies_group, dt):
        self.shootCooldown -= 10 * (dt/100)
        if self.shootCooldown <= 0:
            self.shootCooldown = self.maxShootCooldown
            disparo = Bullet(self.disparoImg, self.angle, self.bulletDamage, self.velocidadBala, self.rect.x, self.rect.y, self, player, False)
            self.bullets_group.add(disparo)

        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]

        if self.distanciaAlJugador > self.minAtackDistance:
            self.current_state.done = True
            self.current_state.next_state = "chasing"
    
    # Método para cambiar de estado
    def change_state(self):
        self.state_name = self.current_state.next_state
        self.current_state.done = False
        left = self.current_state.left

        self.current_state = self.states[self.state_name]
        if left:
            self.current_state.left = True
        else:
            self.current_state.left = False

    # Lógica para determinar si el jugador está dentro del rango de visión
    def player_in_sight(self, world, player):
        dx = player.position().x - self.rect.x
        dy = player.position().y - self.rect.y

        self.distanciaAlJugador = math.sqrt((dx**2) + (dy**2))
        self.angle = -math.degrees(math.atan2(dy, dx))

        self.lineStart = (self.rect.x, self.rect.y)
        
        # Si no hay ningun obstaculo, y player.position() es < self.maxViewDistance, se puede ver. 
        if self.distanciaAlJugador < self.maxViewDistance:
            # Si la en la linea de vision se interpone un obstaculo, no se puede ver al jugador
            tileHitBoxList = world.getTilesList()
            destructibleHitBoxList = world.getDestructiblesList()

            for tile in tileHitBoxList:
                if tile.clipline((self.lineStart, (player.position().centerx, player.position().centery))):
                    return False
                
            for tile in destructibleHitBoxList:
                if tile.clipline((self.lineStart, (player.position().centerx, player.position().centery))):
                    return False
        else:
            return False
        
        # Si no hay un obstaculo de por medio y esta suficientemente cerca, se está viendo al jugador
        # Cambiar al estado de chasing
        if self.state_name == "patrolling":
            self.chaseTime = 120
            self.current_state.next_state = "chasing"
            self.current_state.done = True
    def drawBullets(self, screen):
        pass
    
    def die(self,world, player,cameraOffset,enemies_group):
        enemies_group.remove(self)
        
    def hit(self, damage, deflected):
        self.health -= damage
        self.image = self.hitImage
        if self.health <= 0:
            self.current_state.done = True
            self.current_state.next_state = "die"
            print(self.state_name)
