import pygame

class Bullet():
    def __init__(self, disparoImg, direction, x, y, gv) -> None:
        self.global_vars = gv
        
        self.disparoHitBox = disparoImg.get_rect()
        self.disparoHitBox.x = x
        self.disparoHitBox.y = y

        self.velocidadX = 10
        self.velocidadY = 10

        self.damage = 5

        self.disparoImg = disparoImg

        if direction == "left":
            self.disparoImg = pygame.transform.rotate(pygame.transform.scale(self.disparoImg, (100, 100)), 180)
            self.velocidadY = 0
        elif direction == "right":
            self.disparoImg = pygame.transform.scale(self.disparoImg, (100, 100))
            self.velocidadX = -self.velocidadX
            self.velocidadY = 0
        elif direction == "up":
            self.disparoImg = pygame.transform.rotate(pygame.transform.scale(self.disparoImg, (100, 100)), 90)
            self.velocidadX = 0
        elif direction == "down":
            self.disparoImg = pygame.transform.rotate(pygame.transform.scale(self.disparoImg, (100, 100)), -90)
            self.velocidadX = 0
            self.velocidadY = -self.velocidadY

    def update(self):
        
        self.disparoHitBox.x -= self.velocidadX + self.global_vars.CAMERA_OFFSET_X
        self.disparoHitBox.y -= self.velocidadY + self.global_vars.CAMERA_OFFSET_Y
    
    def draw(self, screen):
        screen.blit(self.disparoImg, self.disparoHitBox)