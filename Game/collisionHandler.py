import pygame

from Constants.constants import MAX_JUMP_HEIGHT

class CollisionHandler(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
    
    # Comprueba colisiones en ambos ejes
    def checkCollisions(self, entity, sequence, dx, dy):
        auxRectH = pygame.Rect(entity.rect.x + dx, entity.rect.y, entity.rect.width, entity.rect.height)
        auxRectV = pygame.Rect(entity.rect.x, entity.rect.y + dy, entity.rect.width, entity.rect.height)
        
        collisionsX = auxRectH.collidelist(sequence)
        collisionsY = auxRectV.collidelist(sequence)

        return (collisionsX,collisionsY)
    

    def checkCollisionsAll(self, entity, world, dx, dy, gravity=True):
        # Si la gravedad esta activada, entity debe definir velY y inAir
        tileHitBoxList = world.getTilesList()
        platformHitBoxList = world.getPlatformsList()
        destructibleHitBoxList = world.getDestructiblesList()

        auxRect = pygame.Rect(entity.rect.x + dx, entity.rect.y, entity.width, entity.height) # Rectangulo auxiliar
        
        tileIndex = auxRect.collidelist(tileHitBoxList) # Colisiones horizontales con terreno

        destructibleIndex = auxRect.collidelist(destructibleHitBoxList) # Colisiones horizontales con destructibles

        if tileIndex >= 0 or destructibleIndex >= 0:
            dx = 0
        
        if gravity:
            auxRect2 = pygame.Rect(entity.rect.x, entity.rect.y + dy, entity.width, entity.height) # Rectangulo auxiliar
            tileIndex2 = auxRect2.collidelist(tileHitBoxList) # Colisiones verticales con terreno
            destructibleIndex2 = auxRect2.collidelist(destructibleHitBoxList) # Colisiones verticales con destructibles
            platformIndex = auxRect2.collidelist(platformHitBoxList) # Colisiones verticales con plataformas
            if tileIndex2 >= 0:
                if entity.velY < 0: #Saltando
                    dy = tileHitBoxList[tileIndex2].bottom - entity.rect.top
                    entity.velY = 0
                elif entity.velY >= 0: #Cayendo o en el suelo
                    dy = tileHitBoxList[tileIndex2].top - entity.rect.bottom
                    print(dy)
                    entity.velY = 0
                    #entity.inAir = False

            if destructibleIndex2 >= 0:
                if entity.velY < 0: #Saltando
                    dy = destructibleHitBoxList[destructibleIndex2].bottom - entity.rect.top
                    entity.velY = 0
                elif entity.velY >= 0: #Cayendo o en el suelo
                    dy = destructibleHitBoxList[destructibleIndex2].top - entity.rect.bottom
                    entity.velY = 0
                    #entity.inAir = False

            if platformHitBoxList[platformIndex].colliderect(entity.rect.x, entity.rect.y + dy, entity.width, entity.height):
                if entity.velY >= 0 and (entity.rect.bottom - platformHitBoxList[platformIndex].top) < 15: #Cayendo
                        dy = - (entity.rect.bottom - platformHitBoxList[platformIndex].top)
                        entity.velY = 0
                        #entity.inAir = False
        
        return (dx, dy)

    def checkHorizontalCollisions(self, entity, world, dx):
        # Si la gravedad esta activada, entity debe definir velY y inAir
        tileHitBoxList = world.getTilesList()
        platformHitBoxList = world.getPlatformsList()
        destructibleHitBoxList = world.getDestructiblesList()

        auxRect = pygame.Rect(entity.rect.x + dx, entity.rect.y, entity.width, entity.height) # Rectangulo auxiliar
        
        tileIndex = auxRect.collidelist(tileHitBoxList) # Colisiones horizontales con terreno

        destructibleIndex = auxRect.collidelist(destructibleHitBoxList) # Colisiones horizontales con destructibles

        if tileIndex >= 0 or destructibleIndex >= 0:
            dx = 0
        
        return dx
    
    def checkVerticalCollisions(self, entity, world, dy, velY, inAir):
        tileHitBoxList = world.getTilesList()
        platformHitBoxList = world.getPlatformsList()
        destructibleHitBoxList = world.getDestructiblesList()
        
        auxRect2 = pygame.Rect(entity.rect.x, entity.rect.y + dy, entity.width, entity.height) # Rectangulo auxiliar
        tileIndex2 = auxRect2.collidelist(tileHitBoxList) # Colisiones verticales con terreno
        destructibleIndex2 = auxRect2.collidelist(destructibleHitBoxList) # Colisiones verticales con destructibles
        platformIndex = auxRect2.collidelist(platformHitBoxList) # Colisiones verticales con plataformas
        if tileIndex2 >= 0:
            if velY < 0: #Saltando
                dy = tileHitBoxList[tileIndex2].bottom - entity.rect.top
                velY = 0
            elif velY >= 0: #Cayendo o en el suelo
                dy = tileHitBoxList[tileIndex2].top - entity.rect.bottom
                velY = 0
                entity.inAir = False


        if destructibleIndex2 >= 0:
            if velY < 0: #Saltando
                dy = destructibleHitBoxList[destructibleIndex2].bottom - entity.rect.top
                velY = 0
            elif velY >= 0: #Cayendo o en el suelo
                dy = destructibleHitBoxList[destructibleIndex2].top - entity.rect.bottom
                velY = 0
                entity.inAir = False


        if platformHitBoxList[platformIndex].colliderect(entity.rect.x, entity.rect.y + dy, entity.width, entity.height):
            if velY >= 0 and (entity.rect.bottom - platformHitBoxList[platformIndex].top) < 15: #Cayendo
                    dy = - (entity.rect.bottom - platformHitBoxList[platformIndex].top)
                    velY = 0
                    entity.inAir = False

        return (dy, velY)