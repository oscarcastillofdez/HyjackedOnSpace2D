import pygame

from global_varsClass import Global_Vars
from aux_functions import *

from button import *
from enemy import *
from player import *
from world import *

def main():

    # Iniciar el juego

    global GAME_OVER
    
    # Iniciar las variables del juego
    pygame.init()
    pygame.display.set_caption("Hyjacked on Space")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
    clock = pygame.time.Clock()
    running = True
    deltaTime = 0
    
    # Iniciar las variables globales
    globalVars = Global_Vars()

    # Iniciar el boton de reseteo
    resetImage = pygame.transform.scale(pygame.image.load('Assets/img/reset.png'),(150,150))
    resetButton = Button(0, 0, resetImage, screen, globalVars)
    
    # Iniciar el jugador, los enemigos y el mundo
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGTH / 2 - 130, screen, globalVars)
    enemies_group = pygame.sprite.Group()
    world = World(world_data,screen,enemies_group, globalVars)
        
    
    # Bucle principal
    
    while running:

        # Si se cierra el juego se acaba el programa
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("gray")

        # Actualizar la posición y estado del jugador
        GAME_OVER = player.update(GAME_OVER,world, enemies_group)
        #screen.blit(BACKGROUND, (0,0))

        # Dibujar el cuadrado en el que el personaje se mueve sin scroll
        #draw_grid(screen)
        
        # Actualiza el mundo segun el scroll y los enemigos se dibujan
        world.update()
        enemies_group.draw(screen)
        
        # Si el juego aun no acabo se actualiza la posicion de los enemigos 
        if GAME_OVER == False:
            enemies_group.update()

        # Si el juego acabo se dibuja el boton de reseteo y si este se pulsa se reinicia el jugador y se sigue con el bucle
        if GAME_OVER == True:
            if resetButton.draw():
                player.reset(500, SCREEN_HEIGTH - 130)
                GAME_OVER = False

        # Actualiza la pantalla
        pygame.display.flip()

        # Cosas
        deltaTime = clock.tick(60) / 1000

    pygame.quit()
    
if __name__=="__main__":
    main()
