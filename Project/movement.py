from cgi import test
from tkinter import XView
from turtle import Screen
from math import sqrt as root
import pygame
import os
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

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800



#Classes---------------------

#Background class
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image,(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Player(pygame.sprite.Sprite):
    def __init__(self, upbutton, leftbutton, rightbutton, playerNumber):
        basic = os.path.realpath("Project/basic.png")
        basic2 = os.path.realpath("Project/basic2.png")
        super(Player, self).__init__()
        self.surf = pygame.Surface((70,101))
        self.surf.fill((255,255,255))
        self.surf = pygame.transform.scale(pygame.image.load(basic).convert(), (70,101))
        self.playerNumber = playerNumber

        if self.playerNumber == 1:
            self.surf = pygame.image.load(basic).convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (70,101))
        else:
            self.surf = pygame.image.load(basic2).convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (70,101))
        self.rect = self.surf.get_rect()
        self.grounded = False
        self.airTime = 0
        self.yVelocity = 0
        self.xVelocity = 0
        self.up = upbutton
        self.left = leftbutton
        self.right = rightbutton
        self.width = 70
        self.height = 101
        self.score = 0
        self.DOUBLEJUMP = 0
        self.playerNumber = playerNumber
    def updateYPos(self):
        self.rect.move_ip(0, self.yVelocity)
        
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        basic = os.path.realpath("Project/basic.png")
        basic2 = os.path.realpath("Project/basic2.png")
        if pressed_keys[self.left]:
            if pressed_keys[K_LSHIFT or K_RSHIFT]:
                self.xVelocity = -10
            else:
                self.xVelocity = -5
            if self.playerNumber == 1: 
                self.surf = pygame.image.load(basic).convert_alpha()
                self.surf = pygame.transform.scale(self.surf, (70,101))
            else: 
                self.surf = pygame.image.load(basic2).convert_alpha()
                self.surf = pygame.transform.scale(self.surf, (70,101))
        elif pressed_keys[self.right]:
            if pressed_keys[K_LSHIFT or K_RSHIFT]:
                self.xVelocity = 10
            else:
                self.xVelocity = 5

            if self.playerNumber == 1:
                self.surf = pygame.transform.flip(pygame.image.load(basic).convert_alpha(), True, False)
                self.surf = pygame.transform.scale(self.surf, (70,101))
            else:
                self.surf = pygame.transform.flip(pygame.image.load(basic2).convert_alpha(), True, False)
                self.surf = pygame.transform.scale(self.surf, (70,101))
        else:
            self.xVelocity = 0
        self.rect.move_ip(self.xVelocity, 0)

        if pressed_keys[self.up]:
            # add double jump - which can only jump twice
            if self.grounded == True:
                self.yVelocity = -15
                self.grounded = False
                self.DOUBLEJUMP = 0
            if self.grounded == False and self.yVelocity > -10 and self.DOUBLEJUMP < 1:
                self.airTime = 0
                self.yVelocity = -15
                self.grounded = False
                self.DOUBLEJUMP = 2


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