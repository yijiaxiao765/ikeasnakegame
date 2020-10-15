#   SNAKE GAME

import pygame
import sys
import time
import random

# BGM
pygame.mixer.init()
pygame.mixer_music.load('./bgm.mp3')
pygame.mixer.music.play(-1, 0.0)
sound = pygame.mixer.Sound('./eat.wav')
# Pygame Init
init_status = pygame.init()
if init_status[1] > 0:
    print("(!) Had {0} initialising errors, exiting... ".format(init_status[1]))
    sys.exit()
else:
    print("(+) Pygame initialised successfully ")

# Play Surface
size = width, height = 640, 320
playSurface = pygame.display.set_mode(size)
pygame.display.set_caption("Ikea Snake Game")

# Colors
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
brown = pygame.Color(165, 42, 42)

# FPS controller
fpsController = pygame.time.Clock()

# Game settings
delta = 10
snakePos = [100, 50]
snakeBody = [[100, 50], [90, 50], [80, 50]]
foodPos = [400, 50]
foodSpawn = True
direction = 'RIGHT'
changeto = ''
score = 0
isGameOver = False
isBgm = True


# Game Over
def gameOver():
    myFont = pygame.font.SysFont('monaco', 72)
    GOsurf = myFont.render("Game Over", True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (320, 25)
    playSurface.blit(GOsurf, GOrect)

    myFont = pygame.font.SysFont('monaco', 56)
    GOsurf = myFont.render("Press P Restart The Game", True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (320, 175)
    playSurface.blit(GOsurf, GOrect)

    showScore(0)
    pygame.display.flip()


# Show Score
def showScore(choice=1):
    SFont = pygame.font.SysFont('monaco', 32)
    Ssurf = SFont.render("Score  :  {0}".format(score), True, black)
    Srect = Ssurf.get_rect()
    if choice == 1:
        Srect.midtop = (80, 10)
    else:
        Srect.midtop = (320, 125)
    playSurface.blit(Ssurf, Srect)


while True:
    fpsController.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                snakePos = [100, 50]
                snakeBody = [[100, 50], [90, 50], [80, 50]]
                foodPos = [400, 50]
                foodSpawn = True
                direction = 'RIGHT'
                changeto = ''
                score = 0
                isGameOver = False
            if event.key == pygame.K_SPACE:
                isBgm = not isBgm
                if isBgm:
                    pygame.mixer.music.play(-1, 0.0)
                else:
                    pygame.mixer.music.stop()
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                changeto = 'RIGHT'
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                changeto = 'LEFT'
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                changeto = 'UP'
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                changeto = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    if isGameOver:
        gameOver()
        pygame.display.flip()
        # fpsController.tick(20)
        continue

    # Validate direction
    if changeto == 'RIGHT' and direction != 'LEFT':
        direction = changeto
    if changeto == 'LEFT' and direction != 'RIGHT':
        direction = changeto
    if changeto == 'UP' and direction != 'DOWN':
        direction = changeto
    if changeto == 'DOWN' and direction != 'UP':
        direction = changeto

    # Update snake position
    if direction == 'RIGHT':
        snakePos[0] += delta
    if direction == 'LEFT':
        snakePos[0] -= delta
    if direction == 'DOWN':
        snakePos[1] += delta
    if direction == 'UP':
        snakePos[1] -= delta

    # Snake body mechanism
    if snakePos == foodPos:
        snakeBody.insert(0, list(snakePos))
        foodSpawn = False
        score += 1
        sound.play()
    else:
        snakeBody.reverse()  # 反转蛇身
        cnt = 1
        for pos in snakeBody:  # 从蛇尾开始，遍历蛇身
            if cnt == len(snakeBody):
                # 蛇头设置为新位置
                snakeBody[cnt - 1] = list(snakePos)
            else:
                # 从蛇尾开始，逐格设置前一格的位置
                snakeBody[cnt - 1] = snakeBody[cnt]
            cnt = cnt + 1
        snakeBody.reverse()  # 还原蛇身
    if foodSpawn == False:
        foodPos = [random.randrange(1, width // 10) * delta, random.randrange(1, height // 10) * delta]
        foodSpawn = True

    playSurface.fill(white)
    for pos in snakeBody:
        pygame.draw.rect(playSurface, green, pygame.Rect(pos[0], pos[1], delta, delta))
    pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0], foodPos[1], delta, delta))

    # Bounds
    if snakePos[0] >= width or snakePos[0] < 0:
        gameOver()
        isGameOver = True
    if snakePos[1] >= height or snakePos[1] < 0:
        gameOver()
        isGameOver = True

    # Self hit
    for block in snakeBody[1:]:
        if snakePos == block:
            gameOver()
            isGameOver = True
    showScore()
    pygame.display.flip()
