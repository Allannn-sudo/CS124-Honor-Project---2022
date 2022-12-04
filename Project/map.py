import pygame
import os

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN
)
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800




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
        dir_path = os.path.dirname(os.path.realpath(__file__))
        blockPath = os.path.join(dir_path, "Block.png")
        # block = os.path.realpath(blockPath)
        image = pygame.image.load(blockPath).convert_alpha()
        image = pygame.transform.scale(image, (40,40))

        surface = pygame.Surface((suface_Width, suface_Height)).convert_alpha()
        for i in range(0, suface_Width, 40):
            for j in range(0, suface_Height, 40):
                surface.blit(image, (i , j))
        self.surf = surface

        self.type = "terrain"
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

def addBlock(type, terrainGroup, obstacleList):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    obs1Path = os.path.join(dir_path, "obs1Button.jpg")
    obs2Path = os.path.join(dir_path, "obs2Button.png")
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    if any(mouse_buttons):
        mousex, mousey = mouse_pos
        if type == "saw_obstacle":
            width = 50
            height = 50
            obj = Terrain(width,height,mousex - width/2, mousey - height/2)
            obj.surf = pygame.transform.scale(pygame.image.load(obs1Path).convert(), (50, 50))
            print("placed saw")
        if type == "trampoline_obstacle":
            width = 100
            height = 50
            obj = Terrain( height,height,mousex - width/2, mousey - height/2)
            obj.surf = pygame.transform.scale(pygame.image.load(obs2Path).convert_alpha(), (100, 50))
        obj.type = type
        terrainGroup.add(obj)
        obstacleList.append(obj)


class Platform(pygame.sprite.Sprite):
    def __init__(self, suface_Width, suface_Height, pos_Width, pos_Height):
        super(Platform, self).__init__()
        self.surf = pygame.Surface((suface_Width, suface_Height))    
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(
            topleft=(
                pos_Width, pos_Height
            )
        )
        dir_path = os.path.dirname(os.path.realpath(__file__))
        blockPath = os.path.join(dir_path, "Block.png")
        image = pygame.image.load(blockPath).convert_alpha()
        image = pygame.transform.scale(image, (40,40))

        surface = pygame.Surface((suface_Width, suface_Height)).convert_alpha()
        for i in range(0, suface_Width, 40):
            for j in range(0, suface_Height, 40):
                surface.blit(image, (i , j))
        self.surf = surface
        
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