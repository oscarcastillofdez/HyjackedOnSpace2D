import pygame
import math

class Bullet():
    def __init__(self, disparoImg, direction, velocidad, x, y) -> None:
        
        self.velocidad = velocidad

        radians = math.radians(direction)

        self.velocidadX = -math.cos(radians) * self.velocidad
        self.velocidadY = math.sin(radians) * self.velocidad

        self.damage = 5

        self.disparoImg = disparoImg
        self.despawnTime = 120
        
        self.disparoImg = pygame.transform.rotate(pygame.transform.scale(self.disparoImg, (100, 100)), direction)

        self.rect = disparoImg.get_rect(center=(100, 10000))
        self.rect.x = x
        self.rect.y = y + 30
        self.rect.width = disparoImg.get_width() / 8
        self.rect.height = disparoImg.get_width() / 8

    def update(self, cameraOffset):
        cameraOffsetX,cameraOffsetY = cameraOffset
        self.rect.x -= self.velocidadX + cameraOffsetX
        self.rect.y -= self.velocidadY + cameraOffsetY

    def checkBulletCollision(self, world, enemies_group):
        objetoColision = pygame.sprite.spritecollide(self, enemies_group, False)

        for objeto in objetoColision:
            enemies_group.remove(objeto)
            return True
        
        tileList = world.getTilesList()
        
        if self.rect.collidelist(tileList) >= 0:
            return True

    
    def checkDespawnTime(self):
        self.despawnTime -= 1
        if self.despawnTime <= 0:
            return True
    
    def draw(self, screen):
        offsetX = self.rect.x - 40
        offsetY = self.rect.y - 40
        
        # Poner self.rect.centerx y self.rect.centery?? Evitaria calcular offset pero no se si funcionara bien
        screen.blit(self.disparoImg, (offsetX, offsetY, self.rect.width, self.rect.height))
        #pygame.draw.rect(screen, (255,255,255), self.rect)

    def bulletPosition(self):
        return self.rect
    