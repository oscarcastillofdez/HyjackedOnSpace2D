import pygame
from global_vars import *

def draw_grid2(screen):
        for line in range(0,10):
            pygame.draw.line(screen, (255, 255, 255), (line * TILE_SIZE, 0), (line * TILE_SIZE, SCREEN_HEIGTH))
            pygame.draw.line(screen, (255, 255, 255), (0, line * TILE_SIZE), (SCREEN_WIDTH, line * TILE_SIZE))

def draw_grid(screen):
        pygame.draw.line(screen, (255, 255, 255), (SCREEN_WIDTH / 6, 0), (SCREEN_WIDTH / 6, SCREEN_HEIGTH))
        pygame.draw.line(screen, (255, 255, 255), (SCREEN_WIDTH - (SCREEN_WIDTH / 6), 0), (SCREEN_WIDTH - (SCREEN_WIDTH / 6), SCREEN_HEIGTH))


# Calcula movimiento en el eje x en una direccion
def move_horizontal(pressed, movement, deltaTime):
    if pressed:
        if movement < MAX_VELOCITY:
            movement += INERTIA
        pressed = False
    else: 
        if movement > INERTIA - 1:
            movement -= INERTIA
        else:
            movement = 0
    return (pressed, movement, movement * deltaTime)
