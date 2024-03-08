import pygame
import math
from Constants.constants import *
from Animations.grenadeExplosion import GrenadeExplosion

class GrenadeDamageArea(pygame.sprite.Sprite):
        def __init__(self, image, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.rect = image.get_rect(center=(100, 10000))
            self.rect.width = image.get_width() * 3
            self.rect.height = image.get_height() * 3
            self.rect.x = x
            self.rect.y = y

        def update(self,x,y):
            self.rect.x = x - self.rect.width / 2
            self.rect.y = y - self.rect.height / 2
            

class Grenade(pygame.sprite.Sprite):
    def __init__(self, image, direction, velocidad, x, y, damage) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.damage = damage
        self.damageArea = GrenadeDamageArea(image,x,y)

        self.velocidad = velocidad

        self.angleR = math.radians(direction)

        self.velocidadX = -math.cos(self.angleR) * self.velocidad
        self.velocidadY = math.sin(self.angleR) * self.velocidad
        
        self.gravity = 1.5
        self.timePassed = 0

        self.damage = 2

        self.image = image
        self.despawnTime = 120
        
        self.image = pygame.transform.rotate(pygame.transform.scale(self.image, (25, 25)), direction)

        self.rect = image.get_rect(center=(100, 10000))
        self.rect.x = x
        self.rect.y = y + 30
        self.rect.width = image.get_width() / 8
        self.rect.height = image.get_width() / 8

        self.animations = []
        self.exploded = False
        self.exploding = False
        self.grenadeExplosion = GrenadeExplosion()
    
    def explode(self, enemies_group, destructibles_group, back_animations,grenades_group, world):
        self.grenadeExplosion.rect.x = self.rect.centerx - 250
        self.grenadeExplosion.rect.y = self.rect.centery - 250

        self.grenadeExplosion.scale((500,500))
        self.grenadeExplosion.play()
        back_animations.add(self.grenadeExplosion)

        destructibles = pygame.sprite.spritecollide(self.damageArea, destructibles_group, False)
        enemies = pygame.sprite.spritecollide(self.damageArea, enemies_group, False)

        for destructible in destructibles:
            destructible.destroy(back_animations,world)
            destructibles_group.remove(destructible)

        for enemy in enemies:
            enemy.hit(self.damage)
        
        grenades_group.remove(self)

    def move(self, cameraOffset, dt, world):
        cameraOffsetX,cameraOffsetY = cameraOffset
        dx = 0
        dy = 0
        self.timePassed += dt/100
        #self.velocidad = self.velocidadX + (self.velocidadY - self.gravity*self.timePassed)
        
        dx = self.velocidadX*self.timePassed
        dy = self.velocidadY*self.timePassed - (0.5*self.gravity*self.timePassed**2)

        tileList = world.getTilesList()
        destructibleHitBoxList = world.getDestructiblesList()

        auxRect = pygame.Rect(self.rect.x - dx, self.rect.y, self.rect.width, self.rect.height)
        auxRect2 = pygame.Rect(self.rect.x, self.rect.y - dy, self.rect.width, self.rect.height)

        tileIndex = auxRect.collidelist(tileList)
        tileIndex2 = auxRect2.collidelist(tileList)

        destructibleIndex = auxRect.collidelist(destructibleHitBoxList)
        destructibleIndex2 = auxRect2.collidelist(destructibleHitBoxList)

        if tileIndex >= 0 or destructibleIndex >= 0:
            dx = 0
            self.velocidadX = 0
            self.velocidadY = 0
        
        if tileIndex2 >= 0 or destructibleIndex2 >= 0:
            self.velocidadX = 0
            self.velocidadY = 0
            self.gravity = 0
            dy = 0

        self.rect.x -= dx + cameraOffsetX
        self.rect.y -= dy + cameraOffsetY

        self.damageArea.update(self.rect.x, self.rect.y)


    def update(self, cameraOffset, dt, world, enemies_group, destructibles_group, grenades_group,back_animations):
        self.move(cameraOffset, dt, world)

        if self.checkDespawnTime():
            self.explode(enemies_group, destructibles_group,back_animations,grenades_group,world)
        
    def checkDespawnTime(self):
        self.despawnTime -= 1
        if self.despawnTime <= 0:
            return True

    def bulletPosition(self):
        return self.rect
    
    def checkIfExploded(self):
        return self.exploded
    
    #def draw(self, screen):
        #pygame.draw.rect(screen, (255,255,255), self.damageArea.rect)
        
        