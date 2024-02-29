import pygame
import sys

from Constants.global_varsClass import Global_Vars
from MovementAndCollisions.aux_functions import *

from Enemies.enemy import *
from Player.player import *
from world import *
from GameStates.menu import Menu
from GameStates.splash import Splash
from GameStates.gameplay import Gameplay
from GameStates.game_over import GameOver
from game import Game

def main():
    # Iniciar las variables globales
    globalVars = Global_Vars()

    # Iniciar la dventana del juego
    pygame.init()
    pygame.display.set_caption("Hyjacked on Space")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
   
    # Iniciar los estados del juego

    states = {
        "MENU": Menu(),
        "SPLASH": Splash(),
        "GAMEPLAY": Gameplay(globalVars),
        "GAME_OVER": GameOver(),
    }
    
    # Iniciar el juego
    game = Game(screen, states, "SPLASH")
    game.run()

    pygame.quit()
    sys.exit()
    
if __name__=="__main__":
    main()