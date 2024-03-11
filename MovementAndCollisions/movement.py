import pygame
from Constants.constants import *

# Calcula movimiento en el eje x en una direccion
def move_horizontal(pressed, movement, deltaTime):
    if pressed:
        if movement < MAX_VELOCITY:
            movement += INERTIA * deltaTime//1000
        elif movement == MAX_VELOCITY + 1:
            movement = MAX_VELOCITY 
        elif movement > MAX_VELOCITY:
            movement -= INERTIA * deltaTime//1000
    else: 
        if movement > INERTIA - 1:
            movement -= INERTIA * deltaTime//1000
        else:
            movement = 0
    return (movement)
