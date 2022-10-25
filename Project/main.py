import pygame
import map
import movement
from cgi import test
from turtle import Screen
from math import sqrt as root
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
    K_w,
    K_a,
    K_s,
    K_d,
)

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((0, 0, 0))

# Move the block up and down at a constant speed
surfaceOne = map.Terrain(200, 300, 0, 600)
surfaceTwo = map.Terrain(225, 350, 350, 500)
surfaceThree = map.Terrain(175, 50, 700, 500)
surfaceFour = map.Terrain(200, 300, 1000, 600)
surfaceFive = map.Terrain(100, 25, 0, 475)
surfaceSix = map.Terrain(100, 25, 150, 375)
surfaceSeven = map.Terrain(100, 175, 475, 425)
surfaceToCreate = map.Terrain(100, 25, 9999999, 99999999999)
surfaceToCreate.surf.fill((255, 255, 255))

gAccel = 6

player = movement.Player()
player1 = movement.Player_1()

all_sprites = pygame.sprite.Group()
all_sprites.add(surfaceOne)
all_sprites.add(surfaceTwo)
all_sprites.add(surfaceThree)
all_sprites.add(surfaceFour)
all_sprites.add(surfaceFive)
all_sprites.add(surfaceSix)
all_sprites.add(surfaceSeven)
all_sprites.add(surfaceToCreate)
all_sprites.add(player)
all_sprites.add(player1)

gravity_obj = pygame.sprite.Group()
gravity_obj.add(player)
gravity_obj.add(player1)

# Add blocks to sprite group
terrain = pygame.sprite.Group()
terrain.add(surfaceOne)
terrain.add(surfaceTwo)
terrain.add(surfaceThree)
terrain.add(surfaceFour)
terrain.add(surfaceFive)
terrain.add(surfaceSix)
terrain.add(surfaceSeven)
terrain.add(surfaceToCreate)

clock = pygame.time.Clock()
FRAME_RATE = 60

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    for entity in gravity_obj:
        if pygame.sprite.spritecollideany(entity, terrain):
            obj = pygame.sprite.spritecollideany(entity, terrain).rect
            if entity.grounded == False:
                # Check if player is less than 50 units into the ground from the top (should be only when player lands on top of terrain)
                if entity.rect.right > obj.left and entity.rect.left < obj.right and entity.rect.bottom < obj.top + 50:
                    entity.grounded = True
                    entity.airTime = 0
                    entity.yVelocity = 0
                    entity.rect.y = obj.top + 1 - entity.rect.h
                # Check if player is more than 50 units into the ground from the top (should be only when player is not on terrain/on the side of the terrain)
                else:
                    # Check which side of terrain player is colliding with
                    # Right
                    if entity.rect.left < obj.right and entity.rect.left > obj.right - 10:
                        entity.rect.left = obj.right
                    # Left
                    if entity.rect.right > obj.left and entity.rect.right < obj.left + 10:
                        entity.rect.right = obj.left
            elif entity.grounded == True:
                entity.airTime = 0
        else:
            entity.grounded = False
            entity.yVelocity = entity.yVelocity + gAccel * entity.airTime
            entity.airTime += 1 / FRAME_RATE

    screen.fill((0, 0, 0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    player.updateYPos()
    player1.update(pressed_keys)
    player1.updateYPos()

    for obj in terrain:
        screen.blit(obj.surf, obj.rect)

    # Move surface three up and down
    surfaceThree.update()
    # Place the surface by mouse click
    surfaceToCreate.update2()

    pygame.display.flip()

    clock.tick(FRAME_RATE)

