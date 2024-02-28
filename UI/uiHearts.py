import pygame

class UIHearts():
    def __init__(self) -> None:
        self.hearts = pygame.transform.scale(pygame.image.load('Assets/img/hearts_3.png').convert_alpha(), (180,100))
        self.rect = self.hearts.get_rect()
        self.rect.x = 30
        self.rect.y = 30
    
    def update(self, observable):
        self.hearts = pygame.transform.scale(pygame.image.load('Assets/img/hearts_'+ str(observable.getHp()) +'.png').convert_alpha(), (180,100))
    
    def draw(self, screen):
        screen.blit(self.hearts, self.rect)
