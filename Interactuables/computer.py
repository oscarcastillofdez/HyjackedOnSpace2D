import pygame

class Computer(pygame.sprite.Sprite):
    def __init__(self,x,y, globalVars):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('Assets/img/ibm5150.png'),(45,45))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.globalVars = globalVars
    
    def interact(self):
        return "Presiona E para interactuar."


    def update(self, player):
        self.rect.x -= self.globalVars.CAMERA_OFFSET_X
        self.rect.y -= self.globalVars.CAMERA_OFFSET_Y
