import pygame

from global_varsClass import Global_Vars
from aux_functions import *

from button import *
from enemy import *
from player import *
from world import *

def main():
    global GAME_OVER
    
    pygame.init()
    pygame.display.set_caption("Hyjacked on Space")
    
    globalVars = Global_Vars()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
    clock = pygame.time.Clock()
    running = True
    deltaTime = 0

    resetImage = pygame.transform.scale(pygame.image.load('Assets/img/reset.png'),(150,150))
    
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGTH / 2 - 130, screen, globalVars)
    enemies_group = pygame.sprite.Group()
    resetButton = Button(0, 0, resetImage, screen, globalVars)
    world = World(world_data,screen,enemies_group, globalVars)
        
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("gray")
        GAME_OVER = player.update(GAME_OVER,world, enemies_group)
        #screen.blit(BACKGROUND, (0,0))
        draw_grid(screen)
        world.update()
        enemies_group.draw(screen)
        
        
        if GAME_OVER == False:
            enemies_group.update()

        if GAME_OVER == True:
            if resetButton.draw():
                player.reset(100, SCREEN_HEIGTH - 130)
                GAME_OVER = False

        pygame.display.flip()

        deltaTime = clock.tick(60) / 1000

    pygame.quit()
    
if __name__=="__main__":
    main()
