from cgi import test
from turtle import Screen
from math import sqrt as root
import pygame
from pygame.locals import (
    RLEACCEL,
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_LSHIFT,
    K_RSHIFT,
)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



#Classes---------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75,150))
        self.surf.fill((255,255,255))
        self.surf = pygame.image.load("basic.jpeg").convert()
        # self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.grounded = False
        self.airTime = 0
        self.yVelocity = 0
    def updateYPos(self):
        self.rect.move_ip(0, self.yVelocity)
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            if pressed_keys[K_LSHIFT or K_RSHIFT]: # add shift for speeding up
                self.rect.move_ip(-10, 0)
            else : 
                self.rect.move_ip(-5, 0)
            # player animation
            self.surf = pygame.image.load("move1.jpeg").convert()
        if pressed_keys[K_RIGHT]:
            if pressed_keys[K_LSHIFT or K_RSHIFT]: # add shift for speeding up
                self.rect.move_ip(10, 0)
            else : 
                self.rect.move_ip(5, 0)
            # player animation
            self.surf = pygame.transform.flip(pygame.image.load("move1.jpeg").convert(), True, False)
        if pressed_keys[K_UP]:
            # add double jump - which can only jump twice
            DOUBLEJUMP = 0
            if self.grounded:
                if (DOUBLEJUMP < 2): 
                    self.grounded = False
                self.yVelocity = -15
                DOUBLEJUMP += 1
                
            if self.yVelocity < 0:
                self.yVelocity = -15


        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
            self.yVelocity = 0
        if self.rect.top >= SCREEN_HEIGHT:
            self.rect.top = SCREEN_HEIGHT

#Terrain code from map.py
class Terrain(pygame.sprite.Sprite):
    def __init__(self, suface_Width, suface_Height, pos_Width, pos_Height):
        super(Terrain, self).__init__()
        self.surf = pygame.Surface((suface_Width, suface_Height))    
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(
            topleft=(
                pos_Width, pos_Height
            )
        )
        self.moving_up = True
    
    #Move the block up and down at a constant speed
    def update(self):
        if self.moving_up == True:
            self.rect.move_ip(0, -3)
        elif self.moving_up == False:
            self.rect.move_ip(0, 3)
        if self.rect.top == 575:
            self.moving_up = True
        if self.rect.top == 200:
            self.moving_up = False

#Initialize Variables?-------
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

gAccel = 6

player = Player()

#temporary
testTerrain = Terrain(175, 175, 0, 500)
testTerrain2 = Terrain(100, 250, 350, 400)
testTerrain3 = Terrain(100, 250, 550, 300)

    #Sprite Groups
all_sprites = pygame.sprite.Group()
gravity_obj = pygame.sprite.Group()
terrain = pygame.sprite.Group()
#add terrain to terrain group when generating terrain using a method?


    #Add to groups
all_sprites.add(player)
all_sprites.add(testTerrain)
all_sprites.add(testTerrain2)
all_sprites.add(testTerrain3)

gravity_obj.add(player)

#temporary
terrain.add(testTerrain)
terrain.add(testTerrain2)
terrain.add(testTerrain3)


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
        if pygame.sprite.spritecollideany(entity, terrain):
            obj = pygame.sprite.spritecollideany(entity, terrain).rect
            if entity.grounded == False:
                #Check if player is less than 50 units into the ground from the top (should be only when player lands on top of terrain)
                if entity.rect.right > obj.left and entity.rect.left < obj.right and entity.rect.bottom < obj.top + 50:
                    entity.grounded = True
                    entity.airTime = 0
                    entity.yVelocity = 0
                    entity.rect.y = obj.top + 1 - entity.rect.h
                #Check if player is more than 50 units into the ground from the top (should be only when player is not on terrain/on the side of the terrain)
                else:
                    #Check which side of terrain player is colliding with
                    #Right
                    if entity.rect.left < obj.right and entity.rect.left > obj.right - 10:
                        entity.rect.left = obj.right
                    #Left
                    if entity.rect.right > obj.left and entity.rect.right < obj.left + 10:
                        entity.rect.right = obj.left
            elif entity.grounded == True:
                entity.airTime = 0
        else:
            entity.grounded = False
            entity.yVelocity = entity.yVelocity + gAccel * entity.airTime
            entity.airTime += 1/FRAME_RATE

    screen.fill((0, 0, 0))
    
    for entity in all_sprites:
        screen.blit(entity.surf,entity.rect)
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    player.updateYPos()
    pygame.display.flip()

    clock.tick(FRAME_RATE)
