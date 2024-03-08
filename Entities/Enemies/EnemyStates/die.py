from Entities.Player.PlayerStates.base import pState
from Game.spritesheet import Spritesheet

class Die(pState):
    def __init__(self, entity):
        super(Die, self).__init__()
        self.animation = Spritesheet('Assets/Images/Entities/aliens.png',(120,120)).get_animation(0,0,24,24,4,(80,80,80))
        self.entity = entity
    
    def update(self, dt, world, player, cameraOffset,enemies_group):
        self.entity.die(world, player, cameraOffset,enemies_group)