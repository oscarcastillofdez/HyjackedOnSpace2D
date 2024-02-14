import pygame
from math import floor
from global_vars import *

class Player():
        def __init__(self,x,y,screen,globalVars):
            self.screen = screen
            self.globalVars = globalVars
            self.reset(x,y)

        
        def update(self, GAME_OVER, world, enemies_group):

            if GAME_OVER == False:
                dx = 0
                dy = 0

                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    dx -= floor(7.5)
                if keys[pygame.K_d]:
                    dx += floor(7.5)
                if keys[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                    self.vel_y = -25
                    self.jumped = True
                if keys[pygame.K_SPACE] == False:
                    self.jumped = False
                

                self.vel_y += 1
                if self.vel_y > 10:
                    self.vel_y = 10
                dy += self.vel_y

                self.in_air = True

                for tile in world.tile_list:
                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0

                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        if self.vel_y < 0: #Saltando
                            dy = tile[1].bottom - self.rect.top
                            self.vel_y = 0
                        elif self.vel_y >= 0: #Callendo
                            dy = tile[1].top - self.rect.bottom
                            self.vel_y = 0
                            self.in_air = False

                    if pygame.sprite.spritecollide(self, enemies_group, False):
                        GAME_OVER = True
                        
                self.globalVars.CAMERA_OFFSET_X = 0

                if self.rect.x > SCREEN_WIDTH / 6 and self.rect.x < SCREEN_WIDTH - (SCREEN_WIDTH / 6):
                    self.rect.x += dx 
                elif self.rect.x + dx > SCREEN_WIDTH / 6 and self.rect.x + dx < SCREEN_WIDTH - (SCREEN_WIDTH / 6):
                    self.rect.x += dx 
                else:
                    self.globalVars.CAMERA_OFFSET_X = dx
                self.rect.y += dy

                if self.rect.bottom > SCREEN_HEIGTH:
                    self.rect.bottom = SCREEN_HEIGTH
                    self.in_air = False
                    dy = 0
            else:
                self.standing = self.dead_image
                

            self.screen.blit(self.standing, self.rect)
            return GAME_OVER

        def reset(self,x,y):
            self.standing = pygame.transform.scale(pygame.image.load("Assets/move1.png"), (100,100))
            self.rect = self.standing.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.width = self.standing.get_width()
            self.height = self.standing.get_height()
            self.vel_y = 0
            self.jumped = False
            self.in_air = True
            self.dead_image = pygame.transform.rotate(self.standing,90)