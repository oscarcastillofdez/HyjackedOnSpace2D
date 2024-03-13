from Entities.Player.PlayerStates.base import pState
from Game.spritesheet import Spritesheet

class Chase(pState):
    def __init__(self, file, entity, scale, coords, color=(0,0,0)):
        super(Chase, self).__init__()
        x,y,w,h,n = coords
        self.animation = Spritesheet(file,scale).get_animation(x,y,w,h,n,color)
        self.entity = entity
    
    def update(self, dt, world, player, cameraOffset,enemies_group):
        self.entity.chase(world, player, cameraOffset,enemies_group)