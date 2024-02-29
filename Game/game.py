import pygame

class Game():
    def __init__(self, screen, states, start_state):
        self.done = False
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.current_state = None
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]
    
    def event_loop(self):
        for event in pygame.event.get():
            self.state.get_event(event)
    
    def change_state(self):
        self.current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state

        # Datos persistentes entre estados. Ej.:(Posicion del jugador/enemigos)
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)

    """
        Esta funcion checkea si hay que cambiar de estado o no
        usando la funcion change_state.
    """
    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.change_state()
        self.state.update(dt)
    
    # Funcion para dibujar todo
    def draw(self):
        self.state.draw(self.screen)
    
    def run(self):
        while not self.done:
            # dt= Tiempo restante para los 60 FPS
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pygame.display.update()
