import pygame
import sys

from MovementAndCollisions.aux_functions import *

from Game.GameStates.menu import Menu
from Game.GameStates.splash import Splash
from Game.GameStates.gameplay import Gameplay
from Game.GameStates.game_over import GameOver
from Game.game import Game

def main():

    # Iniciar la dventana del juego
    pygame.init()
    pygame.display.set_caption("Hyjacked on Space")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
   
    # Iniciar los estados del juego

    states = {
        "MENU": Menu(),
        "SPLASH": Splash(),
        "GAMEPLAY": Gameplay(),
        "GAME_OVER": GameOver(),
    }
    
    # Iniciar el juego
    game = Game(screen, states, "SPLASH")
    game.run()

    pygame.quit()
    sys.exit()
    
if __name__=="__main__":
    main()