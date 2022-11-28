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
    K_a,
    K_s,
    K_d,
    K_w,
)

pygame.init()

SCREEN_WIDTH = 1275
SCREEN_HEIGHT = 800

#Classes---------------------
#Background class
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image,(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


#Player class---------------------
class Player(pygame.sprite.Sprite):
    def __init__(self, upbutton, leftbutton, rightbutton, playerNumber):
        super(Player, self).__init__()
        self.playerNumber = playerNumber
        self.surf = pygame.Surface((60,80))
        self.surf.fill((255,255,255))
        if self.playerNumber == 1:
            self.surf = pygame.image.load("basic.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (60,80))
        else:
            self.surf = pygame.image.load("move2.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (60,80))
        # self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.grounded = False
        self.airTime = 0
        self.yVelocity = 0
        self.up = upbutton
        self.left = leftbutton
        self.right = rightbutton
        self.score = 0

    def updateYPos(self):
        self.rect.move_ip(0, self.yVelocity)
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[self.left]:
            if pressed_keys[K_LSHIFT or K_RSHIFT]: # add shift for speeding up
                self.rect.move_ip(-10, 0)
            else : 
                self.rect.move_ip(-5, 0)
            # player animation
            if self.playerNumber == 1: 
                self.surf = pygame.image.load("move1.png").convert_alpha()
                self.surf = pygame.transform.scale(self.surf, (60,80))
            else: 
                self.surf = pygame.transform.flip(pygame.image.load("move2.jpeg").convert_alpha(), True, False)
                self.surf = pygame.transform.scale(self.surf, (60,80))
        if pressed_keys[self.right]:
            if pressed_keys[K_LSHIFT or K_RSHIFT]: # add shift for speeding up
                self.rect.move_ip(10, 0)
            else: 
                self.rect.move_ip(5, 0)
            # player animation
            if self.playerNumber == 1:
                self.surf = pygame.transform.flip(pygame.image.load("move1.png").convert_alpha(), True, False)
                self.surf = pygame.transform.scale(self.surf, (60,80))
            else:
                self.surf = pygame.image.load("move2.jpeg").convert_alpha()
                self.surf = pygame.transform.scale(self.surf, (60,80))
        if pressed_keys[self.up]:
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


#Classes---------------------
#Background class
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image,(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        
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