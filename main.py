import pygame
import sys

from global_varsClass import Global_Vars
from aux_functions import *

from button import *
from enemy import *
from player import *
from world import *
from gameStates.menu import Menu
from gameStates.splash import Splash
from gameStates.gameplay import Gameplay
from gameStates.game_over import GameOver
from game import Game

def main():
    # Iniciar el juego
    global GAME_OVER
    
    # Iniciar las variables globales
    globalVars = Global_Vars()

    # Iniciar las variables del juego
    pygame.init()
    pygame.display.set_caption("Hyjacked on Space")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
   
    #clock = pygame.time.Clock()
    #running = True
    #deltaTime = 0
    
    """
        codigo nuevo
    """
    states = {
        "MENU": Menu(),
        "SPLASH": Splash(),
        "GAMEPLAY": Gameplay(globalVars),
        "GAME_OVER": GameOver(),
    }
    """
        fin
    """

    """
        codigo nuevo
    """
    game = Game(screen, states, "SPLASH")
    game.run()

    pygame.quit()
    sys.exit()
    
    """
        fin
    """
    
if __name__=="__main__":
    main()
