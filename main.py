import pygame
import sys

from MovementAndCollisions.movement import *

from Game.game import Game
from Constants.constants import *


def main():
    pygame.init()
    
    # Iniciar el juego
    game = Game()
    game.run()

    pygame.quit()
    sys.exit()
    
if __name__=="__main__":
    main()