import pygame
import math

from Animations.bulletImpact import BulletImpact

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, direction, damage, velocidad, x, y, parent, player, deflected) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.velocidad = velocidad # Velocidad de la bala
        self.parent = parent # Entidad (jugador o enemigo) que disparo la bala
        self.player = player # Jugador
        self.direction = direction # Angulo de la bala en gradoss
        self.deflected = deflected # Indica que la bala fue rebotada por un escudo

        # Atributos de imagen y posicion
        self.image = pygame.transform.rotate(image, direction) # Imagen
        self.bulletImpact = BulletImpact() # Carga la animacion de explosion de la bala
        self.rect = image.get_rect(center=(0, 0)) # Posicion de la bala
        self.rect.x = x
        self.rect.y = y + 30
        self.rect.width = image.get_width() / 8 
        self.rect.height = image.get_width() / 8

        # Atributos de direccion y velocidad
        radians = math.radians(direction) # Angulo de la bala en radianes
        self.velocidadX = -math.cos(radians) * self.velocidad # Velocidad de la bala en el eje X
        self.velocidadY = math.sin(radians) * self.velocidad # Velocidad de la bala en el eje Y

        # Atributos de daño
        self.damage = damage # Daño de la bala
        
        # Atributos de control
        self.despawnTime = 120 # Tiempo para que desaparezca por si sola (Evita que se acumulen)
        self.mask = pygame.mask.from_surface(self.image) # Mascara con la que se calculara las colisiones

        
    # Reproduce la animacion de explosion
    def explodeAnimation(self,back_animations):
        self.bulletImpact.rect.x = self.rect.centerx
        self.bulletImpact.rect.y = self.rect.centery

        self.bulletImpact.scale((50,50))
        self.bulletImpact.play()
        back_animations.add(self.bulletImpact)
    
    # Mueve la bala y calcula si choca contra una pared o un enemigo
    def move(self,cameraOffset, dt, world, enemies_group, back_animations,bullets_group):
        # Mueve la bala
        dx = self.velocidadX * (dt/100)
        dy = self.velocidadY * (dt/100)

        self.rect.x -= dx + cameraOffset[0]
        self.rect.y -= dy + cameraOffset[1]

        # Comprueba si choco contra un enemigo 
        # Utiliza la mascara de la bala para calcular la colision con mas precision
        enemigoGolpeado = pygame.sprite.spritecollide(self, enemies_group, False, pygame.sprite.collide_mask)
        
        if not enemies_group.has(self.parent): # Si la disparo el jugador, haz daño a los enemigos
            for enemigo in enemigoGolpeado:
                enemigo.hit(self.damage,self.deflected) # Daño al enemigo
                self.explodeAnimation(back_animations)
                bullets_group.remove(self)
        else: # Si la disparo un enemigo, haz daño al jugador
            if self.rect.colliderect(self.player.position()):
                if not self.player.hit(self.damage): # Daño al jugador
                    # Si lleva escudo, la bala rebota
                    self.player.deflect(self.direction + 180, self.image, self.velocidad, self.damage, self.rect.centerx, self.rect.centery,bullets_group)
                self.player.hit(self.damage)
                self.explodeAnimation(back_animations)
                bullets_group.remove(self)
        
        tileList = world.getTilesList()
        destructibleList = world.getDestructiblesList()
        
        if self.rect.collidelist(tileList) >= 0 or self.rect.collidelist(destructibleList) >= 0: # Si choca contra una pared
            self.explodeAnimation(back_animations)
            bullets_group.remove(self)

    # Calcula movimiento, colision y tiempo de despawn
    def update(self, cameraOffset, dt, world, enemies_group, destructibles_group, bullets_group,back_animations):
        self.move(cameraOffset, dt, world, enemies_group,back_animations,bullets_group)

        self.checkDespawnTime(bullets_group,back_animations)

    # Actualiza y comprueba el tiempo de despawn, eliminando la bala si este se acaba
    def checkDespawnTime(self,bullets_group,back_animations):
        self.despawnTime -= 1
        if self.despawnTime <= 0:
            self.explodeAnimation(back_animations)
            
            bullets_group.remove(self)