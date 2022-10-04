import pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



#Classes---------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75,75))
        self.surf.fill((255,255,255))
        # self.surf = pygame.image.load("{IMAGE PATH}").convert()
        # self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()

#Initialize Variables?-------
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

player = Player()

    #Sprite Groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

clock = pygame.time.Clock()

running = True
#Game Loop-------------------
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    screen.fill((0, 0, 0))
    
    for entity in all_sprites:
        screen.blit(entity.surf,entity.rect)

    pygame.display.flip()

    clock.tick(30)