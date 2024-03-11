from Entities.Player.PlayerStates.base import pState
from Game.spritesheet import Spritesheet

class Attack(pState):
    def __init__(self, file, entity):
        super(Attack, self).__init__()
        self.animation = Spritesheet(file,(120,120)).get_animation(0,96,48,48,2,(80,80,80))
        self.entity = entity
    
    def update(self, dt, world, player, cameraOffset, enemies_group):
        self.entity.attack(world, player, cameraOffset,enemies_group)