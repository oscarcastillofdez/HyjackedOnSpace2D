import pygame

# Inicializa Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ejemplo de texto en Pygame")

# Define colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Carga la fuente
font = pygame.font.Font(None, 36)

# Función para mostrar texto en pantalla
def mostrar_texto(texto, x, y):
    texto_surface = font.render(texto, True, WHITE)
    screen.blit(texto_surface, (x, y))

# Bucle principal del juego
running = True
texto = "Pulsa E para interactuar"
while running:
    screen.fill(BLACK)

    # Verifica eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                texto = "¡Bien hecho!"

    # Muestra el texto en pantalla
    mostrar_texto(texto, 300, 200)

    # Actualiza la pantalla
    pygame.display.flip()

# Sale de Pygame
pygame.quit()
