import pygame
import math
from Constants.constants import *
from Animations.grenadeExplosion import GrenadeExplosion

# Area de explosion
class GrenadeDamageArea(pygame.sprite.Sprite): 
        def __init__(self, image, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.rect = image.get_rect(center=(100, 10000))
            self.rect.width = image.get_width() * 4
            self.rect.height = image.get_height() * 1.5
            self.rect.x = x
            self.rect.y = y - 200

        def update(self,x,y):
            self.rect.x = x - self.rect.width / 2
            self.rect.y = y - self.rect.height / 2 - 40
            
class Grenade(pygame.sprite.Sprite):
    def __init__(self, image, direction, velocidad, x, y, damage, parent, player) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent # Entidad (jugador o enemigo) que lanzo la granada
        self.player = player # Jugador

        # Atributos de imagen y posicion
        self.image = pygame.transform.rotate(pygame.transform.scale(image, (25, 25)), direction) # Imagen de la granada
        self.grenadeExplosion = GrenadeExplosion() # Coge la animacion de explosion de la granada
        self.rect = image.get_rect(center=(100, 10000)) # Posicion
        self.rect.x = x
        self.rect.y = y + 30
        self.rect.width = image.get_width() / 8
        self.rect.height = image.get_width() / 8
        
        # Atributos de direccion y velocidad
        self.velocidad = velocidad # Velocidad general
        self.angleR = math.radians(direction) # Angulo de lanzamiento
        self.velocidadX = -math.cos(self.angleR) * self.velocidad # Velocidad inicial en X
        self.velocidadY = math.sin(self.angleR) * self.velocidad # Velocidad inicial en Y
        self.gravity = 1.5 # Gravedad (Para calcular la parabola)
        self.timePassed = 0 # Tiempo transcurrido desde que se lanzo la granada (para calcular la parabola)

        # Atributos de daño
        self.damage = damage # Daño
        self.damageArea = GrenadeDamageArea(image,x,y) # Coge el area de explosion, area que recibira daño
        
        # Atributos de control
        self.despawnTime = 120 # Tiempo hasta que despawnee (y por ende explote)

    # Provoca el daño y calcula el area afectada
    def explode(self, enemies_group, destructibles_group, back_animations,grenades_group, world,cameraOffset):
        # Se le resta -250 para centrar la animacion
        self.grenadeExplosion.rect.x = self.rect.centerx - 250 
        self.grenadeExplosion.rect.y = self.rect.centery - 250

        self.grenadeExplosion.scale((500,500))
        self.grenadeExplosion.play()
        back_animations.add(self.grenadeExplosion) # Añade la explosion al grupo de animaciones del fondo
        
        # Comprueba colisiones con cajas y y enemigos cercanos
        destructibles = pygame.sprite.spritecollide(self.damageArea, destructibles_group, False)
        enemies = pygame.sprite.spritecollide(self.damageArea, enemies_group, False)

        for destructible in destructibles:
            destructible.destroy(back_animations,world, destructibles_group)

        # Si no la lanzo un enemigo, la lanzo el jugador: Haz daño a enemigos cercanos
        if not enemies_group.has(self.parent):
            for enemy in enemies:
                enemy.hit(self.damage, False)
        else: # Si no la lanzo el jugador, la lanzo un enemigo: Haz daño al jugador si esta en el area de explosion
            if self.damageArea.rect.colliderect(self.player.position()):
                self.player.hit(self.damage)
            
        grenades_group.remove(self) # Quita la granada del grupo
    
    # Calcula movimiento y colisiones de la granada
    def move(self, cameraOffset, dt, world):
        cameraOffsetX,cameraOffsetY = cameraOffset
        dx = 0
        dy = 0
        self.timePassed += dt/100
        
        # Calculo del movimiento parabolico
        # xf = vx*t + xi
        # yf = vy*t + 0.5*g*t² + yi
        # Delta time muy importante para la pela con Vonreg
        dx = (self.velocidadX*self.timePassed) * dt/100
        dy = (self.velocidadY*self.timePassed - (0.5*self.gravity*self.timePassed**2)) * dt/100

        # Calculo de colisiones
        tileList = world.getTilesList()
        platformHitBoxList = world.getPlatformsList()
        destructibleHitBoxList = world.getDestructiblesList()

        auxRect = pygame.Rect(self.rect.x - dx, self.rect.y, self.rect.width, self.rect.height) # Rect auxiliar dx
        auxRect2 = pygame.Rect(self.rect.x, self.rect.y - dy, self.rect.width, self.rect.height) # Rect auxiliar dy

        tileIndex = auxRect.collidelist(tileList) # Colisiones horizontales con terreno
        tileIndex2 = auxRect2.collidelist(tileList) # Colisiones verticales con terreno

        destructibleIndex = auxRect.collidelist(destructibleHitBoxList) # Colisiones horizontales con destructibles
        destructibleIndex2 = auxRect2.collidelist(destructibleHitBoxList) # Colisiones verticales con destructibles
        
        platformIndex = auxRect.collidelist(platformHitBoxList) # Colisiones horizontales con plataformas
        platformIndex2 = auxRect2.collidelist(platformHitBoxList) # Colisiones verticales con plataformas

        # Si choca contra el suelo...
        if tileIndex >= 0 or destructibleIndex >= 0 or platformIndex >= 0: 
            dx = 0
            self.velocidadX = 0
            self.velocidadY = 0

        # Si choca contra una pared...
        if tileIndex2 >= 0 or destructibleIndex2 >= 0 or platformIndex2 >= 0: 
            self.velocidadX = 0
            self.velocidadY = 0
            self.gravity = 0
            dy = 0

        # Mueve la granada
        self.rect.x -= (dx + cameraOffsetX)
        self.rect.y -= (dy + cameraOffsetY)

        # Mueve el area de explosion
        self.damageArea.update(self.rect.x, self.rect.y)

    # Actualiza la bala
    def update(self, cameraOffset, dt, world, enemies_group, destructibles_group, grenades_group,back_animations):
        self.move(cameraOffset, dt, world)

        if self.checkDespawnTime(): # Si se acaba el tiempo de despawn, explota
            self.explode(enemies_group, destructibles_group,back_animations,grenades_group,world,cameraOffset)
    
    # Calcula el tiempo de despawn
    def checkDespawnTime(self):
        self.despawnTime -= 1
        if self.despawnTime <= 0:
            return True