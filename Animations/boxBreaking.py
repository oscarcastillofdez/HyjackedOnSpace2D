from Constants.constants import *
from pyganim import PygAnimation
from Animations.animation import Animation

class BoxBreaking(Animation):
    def __init__(self) -> None:
        # Cargar sprites
        
        self.explosionSpriteList = []
        
        i = 1
        for x in range(5):
            self.explosionSpriteList.append((ANIMATIONS_PATH + 'Box/'+ str(i) +'.png', 100))
            i += 1
        
        super().__init__(self.explosionSpriteList, False)