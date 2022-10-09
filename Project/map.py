import pygame

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen.fill((0, 0, 0))



class Terrain(pygame.sprite.Sprite):
    # #Group for player movement wrote this part for temporary testing
    # def __init__(self):
    #     super(Terrain, self).__init__()
    #     self.surf = pygame.Surface((150,50))    
    #     self.surf.fill((0,255,0))
    #     #temporary terrain placement (create method with position, shape, and color as argument?)
    #     self.rect = self.surf.get_rect(
    #         topleft=(
    #             0, SCREEN_HEIGHT - 100
    #         )
    #     )
    # #I want to create a constructor for each block that accept parameter
    # def update(self, suface_Width, suface_Height, pos_Width, pos_Height):
    #     self.surf = pygame.Surface((suface_Width, suface_Height))
    #     self.rect = self.surf.get_rect(
    #         topleft=(
    #             pos_Width, pos_Height
    #         )
    #     )
#---------------    CHANGED PART
    def __init__(self, suface_Width, suface_Height, pos_Width, pos_Height):
        super(Terrain, self).__init__()
        self.surf = pygame.Surface((suface_Width, suface_Height))    
        self.surf.fill((0,255,0))
        #temporary terrain placement (create method with position, shape, and color as argument?)
        self.rect = self.surf.get_rect(
            topleft=(
                pos_Width, pos_Height
            )
        )
#---------------    CHANGED PART


# surfaceOne = Terrain()
# surfaceTwo = Terrain()
# surfaceThree = Terrain()
# surfaceFour = Terrain()

# surfaceOne.update(175, 175, 0, 500)
# surfaceTwo.update(100, 250, 275, 400)
# surfaceThree.update(100, 25, 450, 500)
# #Also let surfaceThree move up and dow in constant speed later
# surfaceFour.update(175, 100, 625, 500)

#---------------    CHANGED PART
surfaceOne = Terrain(175, 175, 0, 500)
surfaceTwo = Terrain(100, 250, 275, 400)
surfaceThree = Terrain(100, 25, 450, 500)
surfaceFour = Terrain(175, 100, 625, 500)
#---------------


terrain = pygame.sprite.Group()
terrain.add(surfaceOne)
terrain.add(surfaceTwo)
terrain.add(surfaceThree)
terrain.add(surfaceFour)


running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    screen.fill((0,0,0))

    for obj in terrain:
        screen.blit(obj.surf,obj.rect)

    pygame.display.flip()

#Nothing appears in the screen
