import pygame
import map
import movement
import importlib
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

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
screen.fill((0, 0, 0))


white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
green = (0, 255, 0)

surfaceOne = map.Terrain(200, 300, 0, 600)
surfaceTwo = map.Terrain(225, 350, 350, 500)
surfaceThree = map.Platform(175, 50, 700, 500)
surfaceFour = map.Terrain(300, 300, 1000, 600)
surfaceFive = map.Terrain(100, 25, 0, 475)
surfaceSix = map.Terrain(100, 25, 150, 375)
surfaceSeven = map.Terrain(100, 175, 475, 425)


gAccel = 6

player1 = movement.Player(K_UP, K_LEFT, K_RIGHT, 1)
player2 = movement.Player(K_w, K_a, K_d, 2)

BackGround = movement.Background('backGround2.png', [0,0])

all_sprites = pygame.sprite.Group()
all_sprites.add(surfaceOne)
all_sprites.add(surfaceTwo)
all_sprites.add(surfaceThree)
all_sprites.add(surfaceFour)
all_sprites.add(surfaceFive)
all_sprites.add(surfaceSix)
all_sprites.add(surfaceSeven)
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
terrain.add(surfaceFour)
terrain.add(surfaceFive)
terrain.add(surfaceSix)
terrain.add(surfaceSeven)

platform_group = pygame.sprite.Group()
platform_group.add(surfaceThree)

obstacles = []

newGame = 0
#Score
#---------------
class Score(pygame.sprite.Sprite):
    def __init__(self, Player):
        super(Score, self).__init__()
        self.display_surface = screen
        pygame.display.set_caption('Show Text')
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = self.font.render('Player ' + str(Player.playerNumber) + ': ' + str(Player.score), True, green)
        self.textRect = pygame.Rect(0,0, SCREEN_WIDTH,SCREEN_HEIGHT)
        self.scoreNumber = Player.playerNumber
#---------------
score1 = Score(player1)
score2 = Score(player2)
scores = pygame.sprite.Group()
scores.add(score1)
scores.add(score2)

#UI Text
#-----------------
class Text(pygame.sprite.Sprite):
    def __init__(self, textToShow):
        super(Text, self).__init__()
        self.display_surface = screen
        pygame.display.set_caption('Show Text')
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = self.font.render(textToShow, True, green)
        self.textRect = self.text.get_rect()
        print(self.textRect)
        self.textRect.center = (SCREEN_WIDTH/2,0)
gameStatusText = Text('Start')
guiElements = pygame.sprite.Group()
guiElements.add(gameStatusText)



#-----------------
restart_image = pygame.image.load('restartbutton.png').convert_alpha()
obs1_image = pygame.image.load('obs1Button.jpg').convert_alpha()
obs2_image = pygame.transform.scale(pygame.image.load('obs2Button.png').convert_alpha(), (100, 50))
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

        
        screen.blit(self.image, (self.rect.x, self.rect.y))
#-------------------------
restartButton = Button(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, restart_image, 1)
obs1Button = Button(SCREEN_WIDTH - 50, 50, obs1_image, 1)
obs2Button = Button(SCREEN_WIDTH - 50, 150, obs2_image, 1)


clock = pygame.time.Clock()
FRAME_RATE = 60
placeCD = -2
gameStatus = 0
gameTimer = 0
objPlacedInRound = 0
obsTypes = ["terrain", "saw_obstacle", "trampoline_obstacle"]
selectedType = obsTypes[0]



running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    for entity in gravity_obj:
        for obs in obstacles:
            if obs.rect.colliderect(entity.rect.x + entity.xVelocity, entity.rect.y + entity.yVelocity, entity.width, entity.height) or obs.rect.colliderect(entity.rect.x, entity.rect.y + entity.yVelocity, entity.width, entity.height):
                if obs.type == "saw_obstacle": 
                    entity.rect.y = 1500
        for obj in terrain:
            setPosx = entity.xVelocity
            if obj.rect.colliderect(entity.rect.x + entity.xVelocity, entity.rect.y, entity.width, entity.height):
                if entity.xVelocity < 0:
                    entity.rect.left = obj.rect.right
                    entity.xVelocity = 0
                elif entity.xVelocity > 0:
                    entity.rect.right = obj.rect.left
                    entity.xVelocity = 0
                else:
                    entity.rect.centerx = obj.rect.centerx
                    entity.rect.bottom = obj.rect.top
            if obj.rect.colliderect(entity.rect.x, entity.rect.y + entity.yVelocity, entity.width, entity.height):
                if obj.type == "trampoline_obstacle":
                    entity.yVelocity = -15
                    entity.airTime = 0
                elif entity.yVelocity < 0:
                    entity.rect.top = obj.rect.bottom
                    entity.yVelocity = 0
                elif entity.yVelocity > 0:
                    entity.rect.bottom = obj.rect.top
                    entity.yVelocity = 0
                    entity.grounded = True
                entity.airTime = 0
        entity.rect.move_ip(0, entity.yVelocity)
        entity.yVelocity += gAccel * entity.airTime
        entity.airTime += 1 / FRAME_RATE
    
    # check for collision with moving platform
    # we need to put platform in its own sprite group
    # we also need to differentiate dx and dy (change in movement in the x and y direction) from their velocities
    for entity in gravity_obj:
        for platform in platform_group:
            # collision in the x direction
            if platform.rect.colliderect(entity.rect.x + entity.xVelocity, entity.rect.y, entity.width, entity.height):
                entity.grounded = True
            # collision in the y direction
            if platform.rect.colliderect(entity.rect.x, entity.rect.y + entity.yVelocity, entity.width, entity.height):
                # check if below platform
                if abs((entity.rect.top + entity.yVelocity) - platform.rect.bottom) < 50:
                    #entity.yVelocity = platform.rect.bottom - entity.rect.top
                    entity.grounded = True
                # check if above platform
                elif abs((entity.rect.bottom + entity.yVelocity) - platform.rect.top) < 50:
                    entity.rect.bottom = platform.rect.top
                    entity.grounded = True
                    entity.yVelocity = 4
                    entity.airTime = 0
                # if we have sideways platforms, add another if statement for that
    screen.fill((0,0,0))
    screen.blit(BackGround.image, BackGround.rect)

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    pressed_keys = pygame.key.get_pressed()
    
    #Display score text and increase the score
    score1.display_surface.blit(score1.text, score1.textRect)
    score2.display_surface.blit(score2.text, (0, 40))
    gameStatusText.display_surface.blit(gameStatusText.text, (SCREEN_WIDTH/2, 0))

    if placeCD >= 0:
        placeCD += 1
        if placeCD == 100:
            placeCD = -2
    else:
        obs1Button.draw()
        obs2Button.draw()

    gameStatusText.textRect.midtop = (SCREEN_WIDTH/2, 0)
    if gameStatus == 0:
        if objPlacedInRound < 2:
            if objPlacedInRound == 0:
                gameStatusText.text = gameStatusText.font.render("Player 1 Place Obstacle", True, green)
            elif objPlacedInRound == 1:
                gameStatusText.text = gameStatusText.font.render("Player 2 Place Obstacle", True, green)
            mouse_buttons = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            # print(mouse_pos)
            if any(mouse_buttons) and placeCD == -1 and (mouse_pos[0] < SCREEN_WIDTH - 100 or mouse_pos[1] > 200):
                map.addBlock(selectedType, terrain, obstacles)
                placeCD = 0
                objPlacedInRound += 1
            elif obs1Button.clicked_Then_Released == 2:
                placeCD = -1
                obs1Button.clicked_Then_Released = 0
                selectedType = obsTypes[1]
                print(selectedType)
            elif obs2Button.clicked_Then_Released == 2:
                placeCD = -1
                obs2Button.clicked_Then_Released = 0
                selectedType = obsTypes[2]
                print(selectedType)

        if objPlacedInRound == 2:
            objPlacedInRound = 0
            gameStatus = 1
            gameTimer = 0
    if gameStatus == 1:
        placeCD = 50
        if gameTimer != 180:
            gameTimer += 1
            if gameTimer < 60:
                gameStatusText.text = gameStatusText.font.render("3", True, green)
            if gameTimer >= 60 and gameTimer < 120:
                gameStatusText.text = gameStatusText.font.render("2", True, green)
            if gameTimer >= 120 and gameTimer < 180:
                gameStatusText.text = gameStatusText.font.render("1", True, green)
        if gameTimer >= 180:
            if gameTimer >= 180 and gameTimer < 360:
                gameTimer += 1
                gameStatusText.text = gameStatusText.font.render("START", True, green)
            else:
                gameStatusText.text = gameStatusText.font.render("", True, green)
            for player in players:
                if player.rect.top < 800:
                    player.update(pressed_keys)
                #When one of the players reaches the end
                if player.rect.right == SCREEN_WIDTH:
                    #score plus one
                    player.score = player.score + 1
                    gameStatusText.text = gameStatusText.font.render("Player " + str(player.playerNumber) + " wins!", True, green)
                    #update the score text of the player who reaches the end
                    for score in scores:
                        if score.scoreNumber == player.playerNumber:
                            score.text = score.font.render('Player ' + str(player.playerNumber) + ': ' + str(player.score), True, green, black)
                    #Jump to restarting game
                    gameTimer = 0
                    gameStatus = 2
                if player1.rect.top >= 800 and player2.rect.top >= 800:
                    gameStatusText.text = gameStatusText.font.render("Draw!", True, green)
                    gameTimer = 0
                    gameStatus = 2
    if gameStatus == 2:
        placeCD = 50
        #show which player won or if it is a draw (both players died)
        #if a player won, add point
        #after a specific amount of time set gameStatus = 0 to restart
        print(gameTimer)
        if gameTimer >= 0:
            gameTimer += 1
        if gameTimer >= 90:
            restartButton.draw()
            gameTimer = -1
        if gameTimer == -1:
            #Show the restart button
            restartButton.draw() 
            #If the button is clicked, restart the game
            if restartButton.clicked_Then_Released == 2:
                for player in players:
                    player.rect.top = 0
                    player.rect.left = 0
                    player.airTime = 0
                    player.yVelocity = 0
                restartButton.clicked_Then_Released = 0
                placeCD = 99
                gameStatus = 0

    for obj in terrain:
        screen.blit(obj.surf, obj.rect)

    for obj in platform_group:
        screen.blit(obj.surf, obj.rect)

    # Move surface three up and down
    surfaceThree.update()


    pygame.display.flip()

    clock.tick(FRAME_RATE)