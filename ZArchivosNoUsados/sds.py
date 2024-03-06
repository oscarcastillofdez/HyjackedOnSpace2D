import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definir la clase para los enemigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20)) # Tamaño del enemigo
        self.image.fill("red") # Color del enemigo
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH)
        self.rect.y = random.randrange(-100, -40) # Posición inicial fuera de la pantalla
        self.speedy = random.randrange(1, 5) # Velocidad vertical del enemigo

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT + 10: # Elimina los enemigos que salen de la pantalla
            self.rect.x = random.randrange(0, SCREEN_WIDTH)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 5)

# Configurar la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ejemplo de enemigos")

clock = pygame.time.Clock()

# Lista de todos los sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Bucle principal
running = True
while running:
    clock.tick(30) # Framerate

    # Eventos del teclado
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: # Si se presiona una tecla
            if event.key == pygame.K_SPACE: # Si la tecla es la barra espaciadora
                # Crear 10 enemigos y agregarlos a la lista de sprites
                for i in range(10):
                    enemy = Enemy()
                    all_sprites.add(enemy)
                    enemies.add(enemy)

    # Actualizar
    all_sprites.update()

    # Dibujar
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
