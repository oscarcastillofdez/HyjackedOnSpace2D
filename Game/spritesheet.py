import pygame

class Spritesheet():
    def __init__(self, filename, scale):
        self.file = filename
        self.scale = scale
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()

    def get_sprite(self, x,y,w,h):
        sprite = pygame.Surface((w,h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet, (0,0),(x,y,w,h))
        sprite = pygame.transform.scale(sprite, self.scale)
        return sprite

    def get_animation(self, x,y,w,h,n):
        anim = []
        for i in range(n):
            sprite = self.get_sprite(x+w*i,y,w,h)
            sprite.set_colorkey((255,0,0))
            """sprite = pygame.Surface((w,h))
            sprite.blit(self.sprite_sheet, (0,0),(x,y+64*n,w,h))"""
            sprite = pygame.transform.scale(sprite,self.scale)
            anim.append(sprite)
        return anim
    
    def cargar_sprites(self, sprite_ancho, sprite_alto):
        # Obtiene las dimensiones del spritesheet
        spritesheet_ancho, spritesheet_alto = self.sprite_sheet.get_size()

        # Calcula el número de columnas y filas en el spritesheet
        num_columnas = spritesheet_ancho // sprite_ancho
        num_filas = spritesheet_alto // sprite_alto

        # Divide el spritesheet en sprites individuales
        sprites = []
        for fila in range(num_filas):
            for columna in range(num_columnas):
                x = columna * sprite_ancho
                y = fila * sprite_alto
                sprite = self.sprite_sheet.subsurface(pygame.Rect(x, y, sprite_ancho, sprite_alto))
                sprites.append(sprite)

        return sprites