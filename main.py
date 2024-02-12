import pygame

INERTIA = 20
MAX_VELOCITY = 500
GRAVITY = 1
MIN_JUMP_HEIGHT = 20
MAX_JUMP_HEIGHT = 30
SCREEN_WIDTH = 1280
SCREEN_HEIGTH = 720

def move_horizontal(pressed, movement, deltaTime):
    if pressed:
        if movement < MAX_VELOCITY:
            movement += INERTIA
        pressed = False
    else: 
        if movement > INERTIA - 1:
            movement -= INERTIA
        else:
            movement = 0
    return (pressed, movement, movement * deltaTime)


def main():
    pygame.init()
    pygame.display.set_caption("Hyjacked on Space")
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
    clock = pygame.time.Clock()
    running = True
    deltaTime = 0

    TILE_SIZE = 45

    class World():
        def __init__(self,data):
            self.tile_list = []
            suelo = pygame.image.load('Assets/img/tile_1.png')
            
            row_count = 0
            for row in data:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        img = pygame.transform.scale(suelo, (TILE_SIZE, TILE_SIZE))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * TILE_SIZE
                        img_rect.y = row_count * TILE_SIZE
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                    col_count += 1
                row_count += 1

        def draw(self):
            for tile in self.tile_list:
                screen.blit(tile[0], tile[1])
                pygame.draw.rect(screen, (255,255,255), tile[1], 2)

    class Player():
        def __init__(self,x,y):
            self.standing = pygame.transform.scale(pygame.image.load("Assets/move1.png"), (100,100))
            self.playerRect = self.standing.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
            self.playerRect.x = x
            self.playerRect.y = y
            self.vel_y = 0
            self.jumped = False
        
        def update(self):
            dx = 0
            dy = 0

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                dx -= 5
            if keys[pygame.K_d]:
                dx += 5
            if keys[pygame.K_SPACE] and self.jumped == False:
                self.vel_y = -15
                self.jumped = True
            if keys[pygame.K_SPACE] == False:
                self.jumped = False
            
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            self.playerRect.x += dx
            self.playerRect.y += dy

            if self.playerRect.bottom > SCREEN_HEIGTH:
                self.playerRect.bottom = SCREEN_HEIGTH
                dy = 0
            screen.blit(self.standing, self.playerRect)

    world_data = [[1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1],
                  [1,1,0,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1]]
    
    world = World(world_data)
    player = Player(100, SCREEN_HEIGTH - 130)

    def draw_grid():
        for line in range(0,10):
            pygame.draw.line(screen, (255, 255, 255), (line * TILE_SIZE, 0), (line * TILE_SIZE, SCREEN_HEIGTH))
            pygame.draw.line(screen, (255, 255, 255), (0, line * TILE_SIZE), (SCREEN_WIDTH, line * TILE_SIZE))
        
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("blue")
        player.update()
        #screen.blit(BACKGROUND, (0,0))
        #draw_grid()
        world.draw()
        #pygame.draw.rect(screen, (255,255,255), playerRect, 2)

        #for tile in world.tile_list:
        #    if tile[1].colliderect(playerRect.x, playerRect.y, playerRect.width, playerRect.height):
        #        if jumpVelocity < 0:
        #            dy = tile[1].bottom - 
                
        #playerRect = standing.get_rect(center=playerPos)

        pygame.display.flip()

        deltaTime = clock.tick(60) / 1000

    pygame.quit()
    
if __name__=="__main__":
    main()
