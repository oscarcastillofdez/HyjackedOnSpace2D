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
    GAME_OVER = False

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
                    if tile == 2:
                        en = Enemy(col_count * TILE_SIZE, row_count * TILE_SIZE - 52)                    
                        enemies_group.add(en)
                    col_count += 1
                row_count += 1

        def draw(self):
            for tile in self.tile_list:
                screen.blit(tile[0], tile[1])

    class Player():
        def __init__(self,x,y):
            self.standing = pygame.transform.scale(pygame.image.load("Assets/move1.png"), (100,100))
            self.rect = self.standing.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
            self.rect.x = x
            self.rect.y = y
            self.width = self.standing.get_width()
            self.height = self.standing.get_height()
            self.vel_y = 0
            self.jumped = False
            self.dead_image = pygame.transform.rotate(self.standing,90)
        
        def update(self, GAME_OVER):
            if GAME_OVER == False:
                dx = 0
                dy = 0

                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    dx -= 7.5
                if keys[pygame.K_d]:
                    dx += 7.5
                if keys[pygame.K_SPACE] and self.jumped == False:
                    self.vel_y = -25
                    self.jumped = True
                if keys[pygame.K_SPACE] == False:
                    self.jumped = False
                
                self.vel_y += 1
                if self.vel_y > 10:
                    self.vel_y = 10
                dy += self.vel_y

                for tile in world.tile_list:
                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0

                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        if self.vel_y < 0:
                            dy = tile[1].bottom - self.rect.top
                            self.vel_y = 0
                        elif self.vel_y >= 0:
                            dy = tile[1].top - self.rect.bottom
                            self.vel_y = 0

                    if pygame.sprite.spritecollide(self, enemies_group, False):
                        GAME_OVER = True
                        print(GAME_OVER)
                    

                self.rect.x += dx
                self.rect.y += dy

                if self.rect.bottom > SCREEN_HEIGTH:
                    self.rect.bottom = SCREEN_HEIGTH
                    dy = 0
            else:
                self.standing = self.dead_image
                

            screen.blit(self.standing, self.rect)
            return GAME_OVER

    class Enemy(pygame.sprite.Sprite):
        def __init__(self,x,y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(pygame.image.load('Assets/img/pj.png'), (120, 120))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.move_dir = 1
            self.moved = 0

        def update(self):
            self.moved += 1
            if self.moved == 50:
                self.move_dir = -self.move_dir
                self.moved = 0
            self.rect.x += self.move_dir

    world_data = [[1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1],
                  [1,1,0,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,2,0,0,2],
                  [0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],]
    
    player = Player(100, SCREEN_HEIGTH - 130)
    enemies_group = pygame.sprite.Group()
    world = World(world_data)

    def draw_grid():
        for line in range(0,10):
            pygame.draw.line(screen, (255, 255, 255), (line * TILE_SIZE, 0), (line * TILE_SIZE, SCREEN_HEIGTH))
            pygame.draw.line(screen, (255, 255, 255), (0, line * TILE_SIZE), (SCREEN_WIDTH, line * TILE_SIZE))
        
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("gray")
        GAME_OVER = player.update(GAME_OVER)
        #screen.blit(BACKGROUND, (0,0))
        #draw_grid()
        world.draw()
        enemies_group.update()
        enemies_group.draw(screen)

        pygame.display.flip()

        deltaTime = clock.tick(60) / 1000

    pygame.quit()
    
if __name__=="__main__":
    main()
