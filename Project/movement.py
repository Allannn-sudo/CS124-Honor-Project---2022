from cgi import test
from turtle import Screen
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
        self.airTime = 0
        self.yVelocity = 0
    def updateYPos(self):
        self.rect.move_ip(0, self.yVelocity)
    #Movement
    # def update(self, pressed_keys):
        #For jumping, set self.yVelocity to a certain value when button is pressed

class Terrain(pygame.sprite.Sprite):
    def __init__(self):
        super(Terrain, self).__init__()
        self.surf = pygame.Surface((150,50))    
        self.surf.fill((255,124,124))
        self.rect = self.surf.get_rect(
            center=(
                0, SCREEN_HEIGHT
            )
        )

#Initialize Variables?-------
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

gAccel = -0.2

player = Player()
testTerrain = Terrain()

    #Sprite Groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(testTerrain)

gravity_obj = pygame.sprite.Group()
gravity_obj.add(player)
terrain = pygame.sprite.Group()
terrain.add(testTerrain)
#gravity_obj.add

clock = pygame.time.Clock()
FRAME_RATE = 60

running = True
#Game Loop-------------------
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False


    #GRAVITY
    for entity in gravity_obj:
        entity.yVelocity -= gAccel * entity.airTime
        entity.airTime += 1/30

    #NO GRAVITY IF ON TERRAIN
    # for entity in pygame.sprite.groupcollide(gravity_obj,terrain,0,0).keys():
    #     entity.yVelocity = 0


    screen.fill((0, 0, 0))
    
    for entity in all_sprites:
        screen.blit(entity.surf,entity.rect)

    player.updateYPos()

    pygame.display.flip()

    clock.tick(FRAME_RATE)