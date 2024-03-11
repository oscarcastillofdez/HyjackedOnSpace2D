from Constants.constants import *
from pyganim import PygAnimation
from Animations.animation import Animation

class BulletImpact(Animation):
    def __init__(self) -> None:
        # Cargar sprites
        
        self.bulletImpactSpriteList = []
        
        i = 1
        for x in range(4):
            self.bulletImpactSpriteList.append((ANIMATIONS_PATH + '/BulletImpact/'+ str(i) +'.png', 50))
            i += 1
        
        super().__init__(self.bulletImpactSpriteList, False)