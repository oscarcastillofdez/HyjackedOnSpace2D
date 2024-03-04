import threading
import time

class Shield(): 
    def __init__(self, image) -> None:
        self.originalImage = image
        self.shieldImage = image
        self.shieldRect = image.get_rect()
        self.health = 10
        
        self.minTimeWithoutHits = 120
        self.timeWithoutHits = self.minTimeWithoutHits

        self.minChargeDelay = 15
        self.chargeDelay = self.minChargeDelay 

        
    def update(self, player):
        self.shieldRect.x = player.position().x - 30
        self.shieldRect.y = player.position().y - 37

        if self.health < 11:
            self.timeWithoutHits -= 1
            self.chargeDelay -= 1

            if self.timeWithoutHits < 0:
                if self.chargeDelay < 0:
                    self.chargeDelay = self.minChargeDelay
                    self.charge()
                    player.notify()
    
    def draw(self, screen):
        screen.blit(self.shieldImage, self.shieldRect)
        
    def deflect(self, hitImage):
        self.shieldImage = hitImage
        self.iniciar_proceso_de_cambio_de_imagen()
        if not self.health == 0:
            self.health -= 1
        self.timeWithoutHits = self.minTimeWithoutHits
        

    def charge(self):
        self.health += 1


    def getShieldHp(self):
        return self.health

    def cambiar_imagen_despues_de_retraso(self):
        time.sleep(0.2)  # Espera 3 segundos
        self.shieldImage = self.originalImage  # Cambia la imagen después del retraso

    def iniciar_proceso_de_cambio_de_imagen(self):
        thread = threading.Thread(target=self.cambiar_imagen_despues_de_retraso)
        thread.start()
        # Quitarle vida al escudo
        # Cambiar color del escudo a rojo momentaneamente para mostrar que fue golpeado
        # Si se destruye animacion