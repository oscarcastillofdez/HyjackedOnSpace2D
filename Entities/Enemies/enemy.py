from abc import ABC, abstractmethod

import pygame

class Enemy(pygame.sprite.Sprite, ABC):
    def inheriteSprite(self):
        pygame.sprite.Sprite.__init__(self)

    @abstractmethod
    def update(): # Actualiza el enemigo
        pass
    
    @abstractmethod
    def patrol(): # Enemigo patrulla
        pass
    
    @abstractmethod
    def chase(): # Enemigo persigue
        pass
    
    @abstractmethod
    def attack(): # Enemigo ataca**
        pass

    @abstractmethod
    def die(): # Enemigo muere
        pass
    
    @abstractmethod
    def hit(): # Enemigo recibe daño
        pass
    
    #** En attack, Vonreg define attackingMelee y attackingDistance. Arreglar esto para que solo llame a attack
