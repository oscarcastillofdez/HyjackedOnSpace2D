import pygame
from Constants.global_vars import *

def draw_grid2(screen):
        for line in range(0,10):
            pygame.draw.line(screen, (255, 255, 255), (line * TILE_SIZE, 0), (line * TILE_SIZE, SCREEN_HEIGTH))
            pygame.draw.line(screen, (255, 255, 255), (0, line * TILE_SIZE), (SCREEN_WIDTH, line * TILE_SIZE))

def draw_grid(screen):
        pygame.draw.line(screen, (255, 255, 255), (SCREEN_WIDTH / 3, 0), (SCREEN_WIDTH / 3, SCREEN_HEIGTH))
        pygame.draw.line(screen, (255, 255, 255), (SCREEN_WIDTH - (SCREEN_WIDTH / 3), 0), (SCREEN_WIDTH - (SCREEN_WIDTH / 3), SCREEN_HEIGTH))
        pygame.draw.line(screen, (255, 255, 255), (0, SCREEN_HEIGTH / 3), (SCREEN_WIDTH, SCREEN_HEIGTH / 3))
        pygame.draw.line(screen, (255, 255, 255), (0, SCREEN_HEIGTH - (SCREEN_HEIGTH / 3)), (SCREEN_WIDTH, SCREEN_HEIGTH - (SCREEN_HEIGTH / 3)))




# Calcula movimiento en el eje x en una direccion
def move_horizontal(pressed, movement, deltaTime):
    if pressed:
        if movement < MAX_VELOCITY:
            movement += INERTIA
    else: 
        if movement > INERTIA - 1:
            movement -= INERTIA
        else:
            movement = 0
    return (movement, movement * deltaTime/1000)
