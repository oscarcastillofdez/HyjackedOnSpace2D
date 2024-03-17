import threading
import time


class Shield(): 
    def __init__(self, image) -> None:
        # Atributos de imagen y posicion
        self.originalImage = image # Se usa para cambiar entre escudo dañado y no dañado
        self.shieldImage = image 
        self.shieldRect = image.get_rect() # Posicion

        # Atributos de control de energia
        self.energy = 10 # Energia del escudo
        self.minTimeWithoutHits = 120 # Cooldown para la recarga del escudo
        self.timeWithoutHits = self.minTimeWithoutHits
        self.minChargeDelay = 15 # Tiempo entre recarga del escudo
        self.chargeDelay = self.minChargeDelay 

        # Atributos de interfaz
        self.uiShieldObservers = [] # El uiEnergy está observando el escudo
    
    # Actualiza el escudo
    def update(self, player):
        # Se le aplica un offset de -45 y -37 para centrar el escudo en el personaje
        self.shieldRect.x = player.position().x - 45
        self.shieldRect.y = player.position().y - 37

        # Si el escudo está tocado, calcula tiempo desde el ultimo golpe
        if self.energy < 11: 
            self.timeWithoutHits -= 1
            self.chargeDelay -= 1

            # Si paso un tiempo suficiente entre golpes, el escudo se recarga
            if self.timeWithoutHits < 0: 
                if self.chargeDelay < 0:
                    self.chargeDelay = self.minChargeDelay
                    self.charge() # Recarga
                    #player.notify()
    
    # Dibuja el escudo
    def draw(self, screen):
        screen.blit(self.shieldImage, self.shieldRect)

    # Recibe daño (deflect no es el nombre mas apropiado)
    def deflect(self, hitImage):
        self.shieldImage = hitImage
        # Se llama a un thread para que cambie de color (No es lo mas apropiado)
        self.startChangingImageThread() 
        if not self.energy == 0:
            self.energy -= 1
        self.timeWithoutHits = self.minTimeWithoutHits
        self.notify() # Notifica del cambio a UIEnergy

    # Recarga el escudo
    def charge(self):
        self.energy += 1
        self.notify() # Notifica del cambio a UIEnergy

    # Devuelve la vida del escudo
    def getShieldHp(self):
        return self.energy

    def changeImage(self):
        time.sleep(0.2)  # Espera 3 segundos
        self.shieldImage = self.originalImage  # Cambia la imagen después del retraso

    def startChangingImageThread(self):
        thread = threading.Thread(target=self.changeImage)
        thread.start()

    # Añadir observador
    def addObserver(self, observer):
        self.uiShieldObservers.append(observer)

    # Quitar observador
    def delObserver(self, observer):
        self.uiShieldObservers.remove(observer)
    
    # Notificar observadores
    def notify(self):
        for observer in self.uiShieldObservers:
            observer.update(self)