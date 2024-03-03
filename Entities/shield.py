import threading
import time

class Shield(): 
    def __init__(self, image) -> None:
        self.originalImage = image
        self.shieldImage = image
        self.shieldRect = image.get_rect()

        
    def update(self, player):
        self.shieldRect.x = player.position().x - 30
        self.shieldRect.y = player.position().y - 37
    
    def draw(self, screen):
        screen.blit(self.shieldImage, self.shieldRect)
        
    def deflect(self, hitImage):
        self.shieldImage = hitImage
        self.iniciar_proceso_de_cambio_de_imagen()

    def cambiar_imagen_despues_de_retraso(self):
        time.sleep(0.2)  # Espera 3 segundos
        self.shieldImage = self.originalImage  # Cambia la imagen después del retraso

    def iniciar_proceso_de_cambio_de_imagen(self):
        thread = threading.Thread(target=self.cambiar_imagen_despues_de_retraso)
        thread.start()
        # Quitarle vida al escudo
        # Cambiar color del escudo a rojo momentaneamente para mostrar que fue golpeado
        # Si se destruye animacion