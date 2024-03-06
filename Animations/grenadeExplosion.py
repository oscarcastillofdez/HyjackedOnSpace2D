from Constants.constants import *
from pyganim import PygAnimation
from Animations.animation import Animation

class GrenadeExplosion(Animation):
    def __init__(self) -> None:
        # Cargar sprites
        
        self.explosionSpriteList = []
        
        i = 1
        for x in range(15):
            self.explosionSpriteList.append((ANIMATIONS_PATH + '/explosion3/expl'+ str(i) +'.png', 50))
            i += 1
        
        super().__init__(self.explosionSpriteList, False)