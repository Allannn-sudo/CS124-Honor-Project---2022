import pygame

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
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen.fill((0, 0, 0))



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

    #Place block with mouse click
    def addBlock(self, terrainGroup):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if any(mouse_buttons):
            self.rect = self.surf.get_rect(
                center=(
                    mouse_pos
                )
            )
            mousex, mousey = pygame.mouse.get_pos()
            surfaceEight = Terrain(100, 20, mousex-50, mousey-9)
            terrainGroup.add(surfaceEight)

        #screen.blit(self.surf, self.rect)

        
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

#Create blocks
surfaceOne = Terrain(200, 300, 0, 600)
surfaceTwo = Terrain(225, 350, 350, 500)
surfaceThree = Platform(175, 50, 700, 500)
surfaceFour = Terrain(200, 300, 1000, 600)
surfaceFive = Terrain(100, 25, 0, 475)
surfaceSix = Terrain(100, 25, 150, 375)
surfaceSeven = Terrain(100, 175, 475, 425)
surfaceToCreate = Terrain(100, 25, 1200, 900)
surfaceToCreate.surf.fill((255, 255, 255))


#Add blocks to sprite group
terrain = pygame.sprite.Group()
terrain.add(surfaceOne)
terrain.add(surfaceTwo)
#terrain.add(surfaceThree)
terrain.add(surfaceFour)
terrain.add(surfaceFive)
terrain.add(surfaceSix)
terrain.add(surfaceSeven)
terrain.add(surfaceToCreate)

platform_group = pygame.sprite.Group()
platform_group.add(surfaceThree)
