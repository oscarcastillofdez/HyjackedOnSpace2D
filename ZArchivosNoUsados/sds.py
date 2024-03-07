import pygame

pygame.init()
window = pygame.display.set_mode((200, 200))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 100)

counter = 0
text = font.render(str(counter), True, (0, 128, 0))

time_delay = 1000
timer_event = pygame.USEREVENT+1

# main application loop
run = True
while run:
    clock.tick(60)

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == timer_event:
            # recreate text
            counter += 1
            text = font.render(str(counter), True, (0, 128, 0))

    # clear the display
    window.fill((255, 255, 255))

    # draw the scene
    text_rect = text.get_rect(center = window.get_rect().center)   
    window.blit(text, text_rect)

    # update the display
    pygame.display.flip()