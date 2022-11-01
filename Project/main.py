import pygame
import map
import movement
import importlib
#importlib.reload(movement)
#importlib.reload(map)
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
    MOUSEBUTTONUP,
    K_w,
    K_a,
    K_s,
    K_d,
)

pygame.init()

SCREEN_WIDTH = 1275
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((0, 0, 0))

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
green = (0, 255, 0)

# Move the block up and down at a constant speed
surfaceOne = map.Terrain(200, 300, 0, 600)
surfaceTwo = map.Terrain(225, 350, 350, 500)
surfaceThree = map.Terrain(175, 50, 700, 500)
surfaceFour = map.Terrain(300, 300, 1000, 600)
surfaceFive = map.Terrain(100, 25, 0, 475)
surfaceSix = map.Terrain(100, 25, 150, 375)
surfaceSeven = map.Terrain(100, 175, 475, 425)
surfaceToCreate = map.Terrain(100, 25, 1200, 900)
surfaceToCreate.surf.fill((255, 255, 255))


gAccel = 6

player1 = movement.Player(K_UP, K_LEFT, K_RIGHT, 1)
player2 = movement.Player(K_w, K_a, K_d, 2)

all_sprites = pygame.sprite.Group()
all_sprites.add(surfaceOne)
all_sprites.add(surfaceTwo)
all_sprites.add(surfaceThree)
all_sprites.add(surfaceFour)
all_sprites.add(surfaceFive)
all_sprites.add(surfaceSix)
all_sprites.add(surfaceSeven)
all_sprites.add(surfaceToCreate)
all_sprites.add(player1)
all_sprites.add(player2)

players = pygame.sprite.Group()
players.add(player1)
players.add(player2)

gravity_obj = pygame.sprite.Group()
gravity_obj.add(player1)
gravity_obj.add(player2)

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


newGame = True
#Score
#---------------
class Score(pygame.sprite.Sprite):
    def __init__(self, Player):
        super(Score, self).__init__()
        self.display_surface = pygame.display.set_mode((0, 0))
        pygame.display.set_caption('Show Text')
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = self.font.render('Player ' + str(Player.playerNumber) + ': ' + str(Player.score), True, green)
        self.textRect = self.text.get_rect()
        self.scoreNumber = Player.playerNumber
#---------------
score1 = Score(player1)
score2 = Score(player2)
scores = pygame.sprite.Group()
scores.add(score1)
scores.add(score2)


restart_image = pygame.image.load('restartbutton.jpeg').convert_alpha()
#Button
#-------------------------
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False
        self.clicked_Then_Released = 0
    
    def draw(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.clicked_Then_Released = 1
            if pygame.mouse.get_pressed()[0] == 0 and self.clicked_Then_Released == 1:
                self.clicked = False
                self.clicked_Then_Released = 2
            elif pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        
        screen.blit(self.image, (self.rect.x, self.rect.y))
#-------------------------
restartButton = Button(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, restart_image, 1)


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

    for player in players:
        player.update(pressed_keys)
        player.updateYPos()
    
    #Display score text and increase the score
    score1.display_surface.blit(score1.text, score1.textRect)
    score2.display_surface.blit(score2.text, (0, 40))

    #If the game is processing
    if newGame == True:
        #Place block
        if restartButton.clicked == False:
            surfaceToCreate.update2()
        for player in players:
            #When one of the players reaches the end
            if player.rect.right == SCREEN_WIDTH:
                #score plus one
                player.score = player.score + 1
                for score in scores:
                    if score.scoreNumber == player.playerNumber:
                        score.text = score.font.render('Player ' + str(player.playerNumber) + ': ' + str(player.score), True, green, black)
                #Jump to restarting game
                newGame = False

        if player1.rect.top > 800 and player2.rect.top > 800:
            newGame = False

    #If it goes to restarting the game
    if newGame == False:
        #Show the restart button
        restartButton.draw()
        #If the button is clicked, restart the game
        if restartButton.clicked_Then_Released == 2:
            for player in players:
                player.rect.top = 0
                player.rect.left = 0
            restartButton.clicked_Then_Released = 0
            newGame = True
        
    #if newGame == 2:
        #restartButton.draw()
        #if restartButton.clicked == False:
        #restartButton.clicked_Then_Released = 0
        #newGame = 0


    for obj in terrain:
        screen.blit(obj.surf, obj.rect)

    # Move surface three up and down
    surfaceThree.update()


    pygame.display.flip()

    clock.tick(FRAME_RATE)