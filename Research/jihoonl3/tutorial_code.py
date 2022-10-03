import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init();

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

player = Player()

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False;
        elif event.type == QUIT:
            running = False

    screen.fill((0,0,0))

    # surf = pygame.Surface((50,50))
    # surf.fill((0,0,0))
    # rect = surf.get_rect()

    screen.blit(player.surf, player.rect)

    pygame.display.flip()

