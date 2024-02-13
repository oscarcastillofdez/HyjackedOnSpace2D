import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('Assets/img/pj.png'), (120, 120))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_dir = 1
        self.moved = 0
    def update(self):
        self.moved += 1
        if self.moved == 50:
            self.move_dir = -self.move_dir
            self.moved = 0
        self.rect.x += self.move_dir