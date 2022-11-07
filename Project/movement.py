from cgi import test
from tkinter import XView
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
class Player(pygame.sprite.Sprite):
    def __init__(self, upbutton, leftbutton, rightbutton, playerNumber):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75,150))
        self.surf.fill((255,255,255))
        # self.surf = pygame.image.load("basic.jpeg").convert()
        # self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.grounded = False
        self.airTime = 0
        self.yVelocity = 0
        self.xVelocity = 0
        self.up = upbutton
        self.left = leftbutton
        self.right = rightbutton
        self.width = 75
        # self.width = self.image.get_width()
        self.height = 150
        # self.height = self.image.height()
        self.score = 0
        self.playerNumber = playerNumber
    def updateYPos(self):
        self.rect.move_ip(0, self.yVelocity)
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[self.left]:
            if pressed_keys[K_LSHIFT or K_RSHIFT]:
                self.xVelocity = -10
            else:
                self.xVelocity = -5
            # self.surf = pygame.image.load("move1.jpeg").convert()
        elif pressed_keys[self.right]:
            if pressed_keys[K_LSHIFT or K_RSHIFT]:
                self.xVelocity = 10
            else:
                self.xVelocity = 5
            # self.surf = pygame.transform.flip(pygame.image.load("move1.jpeg").convert(), True, False)
        else:
            self.xVelocity = 0
        self.rect.move_ip(self.xVelocity, 0)

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