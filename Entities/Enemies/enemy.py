from abc import ABC, abstractmethod

import pygame

class Enemy(pygame.sprite.Sprite, ABC):
    def inheriteSprite(self):
        pygame.sprite.Sprite.__init__(self)

    @abstractmethod
    def update(self, dt, world, player,cameraOffset, enemies_group): # Actualiza el enemigo
        pass
    
    @abstractmethod
    def patrol(self, world, player,cameraOffset,enemies_group): # Enemigo patrulla
        pass
    
    @abstractmethod
    def chase(self, world, player,cameraOffset,enemies_group): # Enemigo persigue
        pass
    
    @abstractmethod
    def attack(self, world, player,cameraOffset,enemies_group): # Enemigo ataca**
        pass

    @abstractmethod
    def die(self, world, player,cameraOffset,enemies_group): # Enemigo muere
        pass
    
    @abstractmethod
    def hit(self, world, player,cameraOffset,enemies_group): # Enemigo recibe daño
        pass
    
    #** En attack, Vonreg define attackingMelee y attackingDistance. Arreglar esto para que solo llame a attack
