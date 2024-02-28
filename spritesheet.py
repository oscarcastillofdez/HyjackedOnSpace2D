import pygame

class Spritesheet():
    def __init__(self, filename, scale):
        self.file = filename
        self.scale = scale
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()

    def get_sprite(self, x,y,w,h):
        sprite = pygame.Surface((w,h))
        #sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet, (0,0),(x,y,w,h))
        sprite = pygame.transform.scale(sprite, (100,100))
        return sprite

    def get_animation(self, x,y,w,h,n):
        anim = []
        for i in range(n):
            sprite = self.get_sprite(x+64*i,y,w,h)
            sprite.set_colorkey((255,0,0))
            """sprite = pygame.Surface((w,h))
            sprite.blit(self.sprite_sheet, (0,0),(x,y+64*n,w,h))"""
            sprite = pygame.transform.scale(sprite,(100,100))
            anim.append(sprite)
        return anim