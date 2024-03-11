import pygame
import math

from Animations.bulletImpact import BulletImpact

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, direction, damage, velocidad, x, y, parent, player) -> None:
        pygame.sprite.Sprite.__init__(self)
        
        self.velocidad = velocidad
        self.parent = parent
        self.player = player

        radians = math.radians(direction)

        self.velocidadX = -math.cos(radians) * self.velocidad
        self.velocidadY = math.sin(radians) * self.velocidad

        self.damage = damage

        self.despawnTime = 120
        
        self.image = pygame.transform.rotate(image, direction)
        self.bulletImpact = BulletImpact()
        self.rect = image.get_rect(center=(100, 10000))
        self.rect.x = x
        self.rect.y = y + 30

        self.hitboxRect = image.get_rect(center=(100, 10000))

        self.rect.width = image.get_width() / 8
        self.rect.height = image.get_width() / 8
    
    def explodeAnimation(self,back_animations):
        self.bulletImpact.rect.x = self.rect.centerx
        self.bulletImpact.rect.y = self.rect.centery

        self.bulletImpact.scale((50,50))
        self.bulletImpact.play()
        back_animations.add(self.bulletImpact)
    def move(self,cameraOffset, dt, world, enemies_group, back_animations,bullets_group):
        self.rect.x -= self.velocidadX + cameraOffset[0]
        self.rect.y -= self.velocidadY + cameraOffset[1]

        self.hitboxRect.x = self.rect.x - 30
        self.hitboxRect.y = self.rect.y


        enemigoGolpeado = pygame.sprite.spritecollide(self, enemies_group, False)

        if not enemies_group.has(self.parent): # Si la bala no la disparo un enemigo, la disparo el jugador
            for enemigo in enemigoGolpeado:
                enemigo.hit(self.damage)
                self.explodeAnimation(back_animations)
                #enemies_group.remove(objeto)
                bullets_group.remove(self)
        else: 
            if self.rect.colliderect(self.player):
                self.explodeAnimation(back_animations)
                self.player.hit(self.damage)
        
        tileList = world.getTilesList()
        
        if self.rect.collidelist(tileList) >= 0:
            self.explodeAnimation(back_animations)
            bullets_group.remove(self)

    def update(self, cameraOffset, dt, world, enemies_group, destructibles_group, bullets_group,back_animations):
        self.move(cameraOffset, dt, world, enemies_group,back_animations,bullets_group)

        self.checkDespawnTime(bullets_group,back_animations)

    def checkDespawnTime(self,bullets_group,back_animations):
        self.despawnTime -= 1
        if self.despawnTime <= 0:
            self.explodeAnimation(back_animations)
            
            bullets_group.remove(self)
    
    def draw(self, screen):
        offsetX = self.rect.x - 40
        offsetY = self.rect.y - 40
        
        # Poner self.rect.centerx y self.rect.centery?? Evitaria calcular offset pero no se si funcionara bien
        #screen.blit(self.image, (offsetX, offsetY, self.rect.width, self.rect.height))
        pygame.draw.rect(screen, (255,255,255), self.hitboxRect)

    def bulletPosition(self):
        return self.rect
    