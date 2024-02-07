import pygame

def main():
    pygame.init()
    pygame.display.set_caption("Hyjacked on Space")
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    deltaTime = 0

    jumping = False
    left = False
    leftMov = 0
    right = False
    rightMov = 0
    INERTIA = 20
    MAX_VELOCITY = 500
    GRAVITY = 1
    JUMP_HEIGHT = 20
    jumpVelocity = JUMP_HEIGHT

    BACKGROUND = pygame.image.load("Assets/space/spr_big_meteor.png")
    standing = pygame.transform.scale(pygame.image.load("Assets/move1.png"), (100,100))

    
    player_rect = standing.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
    #player_pos = X_POS, Y_POS
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("blue")
        screen.blit(standing, player_rect)
        screen.blit(BACKGROUND, (0,0))
        # fill the screen with a color to wipe away anything from last frame


        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            left = True
        if keys[pygame.K_d]:
            right = True
        if keys[pygame.K_SPACE]:
            jumping = True

        if left:
            if leftMov < MAX_VELOCITY:
                leftMov += INERTIA
            left = False
        else: 
            if leftMov > INERTIA - 1:
                leftMov -= INERTIA
            else:
                leftMov = 0
        playerPos.x -= leftMov * deltaTime

        if right:
            if rightMov < MAX_VELOCITY:
                rightMov += INERTIA
            right = False
        else: 
            if rightMov > INERTIA -1:
                rightMov -= INERTIA
        playerPos.x += rightMov * deltaTime
        
        if jumping:
            playerPos.y -= jumpVelocity
            jumpVelocity -= GRAVITY
            if jumpVelocity < -JUMP_HEIGHT:
                jumping = False
                jumpVelocity = JUMP_HEIGHT
                

        player_rect = standing.get_rect(center=player_pos)

        player_rect = standing.get_rect(center=player_pos)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        deltaTime = clock.tick(60) / 1000

    pygame.quit()
    
if __name__=="__main__":
    main()
