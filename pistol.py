import pygame
from player import Player
from playerAbstract import PlayerAbstract
from bullet import Bullet

class Pistol(PlayerAbstract):
    def __init__(self, player):
        self.player = player
        self.disparosList = []
        self.coolDown = 30
        
        self.disparoImg = pygame.image.load('Assets/img/lazer_1.png')

    def move_left(self):
        self.player.move_left()
    
    def move_right(self):
        self.player.move_right()
    
    def jump(self):
        self.player.jump()
    
    def getHp(self):
        self.player.getHp()
    
    def checkHit(self, enemies_group):
        self.player.checkHit(enemies_group)
    
    def update(self, world, globalVars, dt):
        self.player.update(world, globalVars, dt)
        self.coolDown -= 1

        for disparo in self.disparosList:
            disparo.update()

    def shoot(self, direction, gv):
        if self.coolDown <= 0:
            self.coolDown = 30

            disparo = Bullet(self.disparoImg, direction, self.player.rect.x, self.player.rect.y, gv)
            self.disparosList.append(disparo)

    def draw(self, screen):
        self.player.draw(screen)

        for disparo in self.disparosList:
            disparo.draw(screen)

    def checkGunPick(self, world):
        return self.player.checkGunPick(world)