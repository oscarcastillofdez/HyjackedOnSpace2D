import pygame

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
    