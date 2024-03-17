from collections import defaultdict
import pygame
from Constants.constants import *
from .Scenes.splash import Splash
from .Scenes.options import Settings

class Game():
    # Director
    def __init__(self):
        # Iniciar la ventana del juego
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
        pygame.display.set_caption("Hyjacked on Space")

        self.clock = pygame.time.Clock()
        self.fps = 60

        # Pila de escenas para el patron director
        self.pila = []
        self.escena_done = False

        # Variable para salir del juego
        self.done = False

        # Lista de joysticks conectados
        #self.joysticks = defaultdict(list)
        self.joysticks = {}

        # Ajustes musica y sonidos
        self.music_volume = 1
        self.sounds_volume = 1

    
    def loop(self, scene):
        self.escena_done = False
        # Eliminamos todos los eventos producidos antes de entrar en el bucle
        pygame.event.clear()

        while not self.escena_done:
            # dt= Tiempo restante para los 60 FPS
            dt = self.clock.tick(self.fps)

            # Eventos
            scene.events(pygame.event.get(), pygame.key.get_pressed(), self.joysticks)
            
            # Actualizamos escena
            scene.update(dt)

            #Dibujamos
            scene.draw(self.screen)
            pygame.display.update()
            # pygame.display.flip()

    def run(self):

        firstScene = Splash(self)
        self.pila.append(firstScene)

        self.escena_done = False
        # Eliminamos todos los eventos producidos antes de entrar en el bucle
        pygame.event.clear()

        while (len(self.pila)>0):
            escena = self.pila[len(self.pila)-1]

            self.loop(escena)

    # METODOS DE CONTROL DE ESCENAS
        # Para indicar que una escena ha acabado
    def finishScene(self):
        self.escena_done = True

        if(len(self.pila)>0):
            self.pila.pop()

        # Para salir de la aplicacion
    def endApplication(self):
        self.pila = []
        self.escena_done = True

        # Para indicar que una escena quiere transitar a otra
    def changeScene(self, scene):
        self.finishScene()
        self.pila.append(scene)

        # Para indicar que una escena quiere transitar a otra Y VOLVER
    def stackScene(self, scene):
        self.escena_done = True
        self.pila.append(scene)