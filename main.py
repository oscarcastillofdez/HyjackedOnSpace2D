import pygame

INERTIA = 20
MAX_VELOCITY = 500
GRAVITY = 1
MIN_JUMP_HEIGHT = 20
MAX_JUMP_HEIGHT = 30

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
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    deltaTime = 0

    jumping = False
    left = False
    leftMov = 0
    right = False
    rightMov = 0
    jumpVelocity = MIN_JUMP_HEIGHT

    BACKGROUND = pygame.image.load("Assets/space/spr_big_meteor.png")
    standing = pygame.transform.scale(pygame.image.load("Assets/move1.png"), (100,100))

    
    playerRect = standing.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
    #player_pos = X_POS, Y_POS
    playerPos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("blue")
        screen.blit(standing, playerRect)
        screen.blit(BACKGROUND, (0,0))
        # fill the screen with a color to wipe away anything from last frame


        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            left = True
        if keys[pygame.K_d]:
            right = True
        if keys[pygame.K_SPACE]:
            jumping = True

        left, leftMov, newPosLeft = move_horizontal(left, leftMov, deltaTime)
        right, rightMov, newPosRight = move_horizontal(right, rightMov, deltaTime)
        playerPos.x += (newPosRight- newPosLeft)

        if jumping:
            playerPos.y -= jumpVelocity
            jumpVelocity -= GRAVITY
            if jumpVelocity < -MIN_JUMP_HEIGHT:
                jumping = False
                jumpVelocity = MIN_JUMP_HEIGHT
                

        playerRect = standing.get_rect(center=playerPos)

        playerRect = standing.get_rect(center=playerPos)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        deltaTime = clock.tick(60) / 1000

    pygame.quit()
    
if __name__=="__main__":
    main()
