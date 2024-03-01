import pygame
from .entity import Entity
import math

from Entities.bullet import Bullet
class FlyingEnemy(pygame.sprite.Sprite, Entity):
    def __init__(self,x,y,globalVars) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('Assets/img/pj.png'), (120, 120))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 100
        self.patrollingchasingSpeed = 1
        self.image_orig = pygame.transform.scale(pygame.image.load('Assets/img/pj.png'), (120, 120))
        self.moved = 0
        self.globalVars = globalVars
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.inAir = True
        self.velY = 0
        self.chasingSpeed = 4
        self.viewDirection = 1
        self.chaseTime = 120
        self.maxViewDistance = 600
        self.minAtackDistance = 300
        self.distanciaAlJugador = 0

        self.shootCooldown = 60
        self.disparoImg = pygame.image.load('Assets/img/lazer_24.png')
        self.disparosList = []
        self.angle = 0
        self.velocidadBala = 10
        
        # Maxima y minima altura que puede volar respecto a su posicion rect.y de respawn
        self.maxFlyingHeight = 10
        self.minFlyingHeight = -5
        
        # Define los estados posibles
        self.states = {"patrolling": self.patrol,
                       "chasing": self.chase,
                       "attacking": self.attack}
        
        # Inicializa el estado actual
        self.current_state = "patrolling"

        self.lineStart = (self.rect.centerx, self.rect.centery)
        #self.disparoImg = pygame.image.load('Assets/img/lazer_1.png')

    def checkBulletCollision2(self, world, player, disparo):
        if disparo.bulletPosition().colliderect(player.position()):
            player.hit()
            return True
        
        for tile in world.terrainHitBoxList:
            if tile.colliderect(disparo.bulletPosition()):
                return True
                
    def update(self, world, player):
        for disparo in self.disparosList:
            disparo.update()
            if self.checkBulletCollision2(world, player, disparo) or disparo.checkDespawnTime():
                self.disparosList.remove(disparo)
                del disparo

        self.states[self.current_state](world, player)
        self.player_in_sight(world, player)

    def patrol(self, world, player):
        # Comportamiento cuando está patrullando
        dy = 0

        self.inAir = True
        self.moved += 1
        if self.moved >= 400:
            self.viewDirection = -self.viewDirection
            self.patrollingchasingSpeed = -self.patrollingchasingSpeed
            self.moved = 0

        
        # Se calculan las colisiones en ambos ejes
        for tile in world.terrainHitBoxList:
            if tile.colliderect(self.rect.x + self.patrollingchasingSpeed, self.rect.y, self.width, self.height):
                self.patrollingchasingSpeed = -self.patrollingchasingSpeed
                self.viewDirection = -self.viewDirection
            
            if tile.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.velY < 0: #Saltando
                        dy = tile.bottom - self.rect.top
                        self.velY = 0
                    elif self.velY >= 0: #Cayendo
                        dy = tile.top - self.rect.bottom
                        self.velY = 0
                        self.inAir = False

        self.rect.x += self.patrollingchasingSpeed - self.globalVars.CAMERA_OFFSET_X
        self.rect.y += dy - self.globalVars.CAMERA_OFFSET_Y

    
    def chase(self, world, player):
        self.chaseTime -= 1

        if self.chaseTime <= 0:
            self.change_state("patrolling")
            
        self.moved = 0

        if player.position().x > self.rect.x:
            self.viewDirection = 1
            self.moved -= self.chasingSpeed

        if player.position().x < self.rect.x:
            self.viewDirection = -1
            self.moved += self.chasingSpeed

        for tile in world.terrainHitBoxList:
            if tile.colliderect(self.rect.x - self.moved, self.rect.y, self.width, self.height):
                self.moved = 0

        self.rect.x -= self.globalVars.CAMERA_OFFSET_X
        self.rect.y -= self.globalVars.CAMERA_OFFSET_Y
        
        self.rect.x -= self.moved

        print("DISTANCIA AL JUGADOR: " + str(self.distanciaAlJugador))
        print("DISTANCIA MINIMA DE ATAQUE: " + str(self.minAtackDistance))

        if self.distanciaAlJugador < self.minAtackDistance:
            self.change_state("attacking")

    
    def attack(self, world, player):
        # Disparar cada x segundos
        

        self.shootCooldown -= 1
        if self.shootCooldown <= 0:
            self.shootCooldown = 30
            print(self.angle)
            disparo = Bullet(self.disparoImg, self.angle, self.velocidadBala, self.rect.x, self.rect.y, world.globalVars)
            self.disparosList.append(disparo)

        self.rect.x -= self.globalVars.CAMERA_OFFSET_X
        self.rect.y -= self.globalVars.CAMERA_OFFSET_Y

        if self.distanciaAlJugador > self.minAtackDistance:
            self.change_state("chasing")
    
    def drawBullets(self, screen):
        for disparo in self.disparosList:
            disparo.draw(screen)
            
    # Método para cambiar de estado
    def change_state(self, new_state):
        self.current_state = new_state

    # Lógica para determinar si el jugador está dentro del rango de visión
    def player_in_sight(self, world, player):
        dx = player.position().centerx - self.rect.centerx
        dy = player.position().centery - self.rect.centery

        self.distanciaAlJugador = math.sqrt((dx**2) + (dy**2))
        self.angle = -math.degrees(math.atan2(dy, dx))

        self.lineStart = (self.rect.centerx, self.rect.centery)
        
        # Si no hay ningun obstaculo, y player.position() es < self.maxViewDistance, se puede ver. 
        if self.distanciaAlJugador < self.maxViewDistance:
            # Si la en la linea de vision se interpone un obstaculo, no se puede ver al jugador
            for tile in world.terrainHitBoxList:
                if tile.clipline((self.lineStart, (player.position().centerx, player.position().centery))):
                    return False
        else:
            return False
        
        # Si no hay un obstaculo de por medio y esta suficientemente cerca, se está viendo al jugador
        # Cambiar al estado de chasing
        if self.current_state == "patrolling":
            self.chaseTime = 120
            self.change_state("chasing")
        