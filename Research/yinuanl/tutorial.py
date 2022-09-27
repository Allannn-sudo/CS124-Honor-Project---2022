
#Setting up
import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

pygame.init()

# Drawing window
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# Run until ask to quit
running = True
while running: 

    #Test if close button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the background with a pretty color
    screen.fill((178, 234, 252))

    # Draw a purple circle in the center
    pygame.draw.circle(screen, (207, 167, 233), (300, 200), 75)

    #Flip the display
    pygame.display.flip()

# quit
pygame.quit()


