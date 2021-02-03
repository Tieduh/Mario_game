import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

start_ticks = pygame.time.get_ticks()

# create window
screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("mario")
icon = pygame.image.load("img/super_mario.png")
pygame.display.set_icon(icon)

background = pygame.image.load("img/background.png")

# background sound
background_music = mixer.music.load("sound/background.wav")
mixer.music.play(-1)

start_time = None
game_start = 377.
clock = pygame.time.Clock()
delta = clock.tick(30)


# Player
playerImg = pygame.image.load("img/mario.png")
playerX = 370
playerY = 454
playerX_change = 0
playerY_change = 0

# Koopa
koopaImg = []
koopaX = []
koopaY = []
koopaX_change = []
koopaY_change = []
num_of_koopas = 6

for i in range(num_of_koopas):
    koopaImg.append(pygame.image.load("img/koopa.png"))
    koopaX.append(random.randint(0, 736))
    koopaY.append(random.randint(50, 150))
    koopaX_change.append(5)
    koopaY_change.append(40)

# fireball
# ready stat means you can't see the fireball on the screen
# fire stat means the fireball is moving
fireballImg = pygame.image.load("img/fire/fireball1.png")
fireballX = 0
fireballY = 440
fireballX_change = 0
fireballY_change = 10
fireball_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('font/SuperMario256.ttf', 32)

textX = 10
textY = 10

# game over text
game_over_font = pygame.font.Font('font/SuperMario256.ttf', 100)



def show_score(x,y):
    score = font.render("Innocent turtles murdered: " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = game_over_font.render("GAME OVER ", True, (255, 0, 0))
    screen.blit(over_text, (90, 250))

def player(x,y):
    screen.blit(playerImg, (x, y))


def koopa(x,y,i):
    screen.blit(koopaImg[i],(x,y))


def fire_ball(x, y):
    global fireball_state
    fireball_state = "fire"
    screen.blit(fireballImg, (x + 16, y + 10))


def isCollision(koopaX, koopaY, fireballX, fireballY):
    distance = math.sqrt((math.pow(koopaX-fireballX, 2)) + (math.pow(koopaY-fireballY, 2)))
    if distance <= 27:
        return True
    else:
        return False


# Clouds
cloud1Img = pygame.image.load("img/clouds/cloud_1.png")
cloud1X = 650
cloud1Y = 200

cloud2Img = pygame.image.load("img/clouds/cloud_2.png")
cloud2X = 50
cloud2Y = 100

cloud3Img = pygame.image.load("img/clouds/cloud_3.png")
cloud3X = 550
cloud3Y = 30

def clouds():
    screen.blit(cloud1Img, (cloud1X, cloud1Y))
    screen.blit(cloud2Img, (cloud2X, cloud2Y))
    screen.blit(cloud3Img, (cloud3X, cloud3Y))


# game loop
running = True
while running:
    screen.fill((0,0,0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check if right of left
        if event.type == pygame.KEYDOWN:
            print("A keystroke has been pressed")
            if event.key == pygame.K_LEFT:
                playerImg = pygame.image.load("img/mario_l.png")
                playerX_change = -5
                print("Left arrow is pressed")
            if event.key == pygame.K_RIGHT:
                playerImg = pygame.image.load("img/mario_r.png")
                playerX_change = 5
                print("Right arrow is pressed")
            if event.key == pygame.K_SPACE:
                if fireball_state == "ready":
                    fireball_sound = mixer.Sound('sound/fireball.wav')
                    fireball_sound.play()
                    # get the current x coordinate of mario
                    fireballX = playerX
                    fire_ball(playerX, fireballY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                print("Keystroke has been released")

    clouds()
    # 5 = 5 + -0.1 -> 5=5 - 0.1
    # 5 =5 + 0.1
    playerX += playerX_change
    if playerX <= 0:
            playerX = 0
    elif playerX >= 736:
        playerX = 736

        # koopa movement
    for i in range(num_of_koopas):

        # game over
        if koopaY[i] > 440:
            playerY += playerY_change
            playerImg = pygame.image.load("img/mario_death.png")
            playerY_change = 10
            playerX_change = 0
            if playerY == 466:
                playerY_change = -1
            for j in range(num_of_koopas):
                koopaY[j] = 2000
                start_time = pygame.time.get_ticks()
                mixer.music.set_volume(0)
                game_over = mixer.Sound('sound/game_over.wav')
                game_over.play()
                game_start -= delta
                if game_start < 0:
                    game_over.set_volume(0)
            game_over_text()
            break

        koopaX[i] += koopaX_change[i]
        if koopaX[i] <= 0:
            koopaImg[i] = pygame.image.load("img/koopa_R.png")
            koopaX_change[i] = 10
            koopaY[i] += koopaY_change[i]
        elif koopaX[i] >= 736:
            koopaImg[i] = pygame.image.load("img/koopa_L.png")
            koopaX_change[i] = -10
            koopaY[i] += koopaY_change[i]
        elif koopaY[i] >= 454:
            koopaY[i] = 454
            koopaY_change[i] = 0

        # collision
        collision = isCollision(koopaX[i], koopaY[i], fireballX, fireballY)
        if collision:
            hit_sound = mixer.Sound('sound/hit.wav')
            hit_sound.play()
            fireballY = 480
            fireball_state = "ready"
            score_value += 1
            #koopaImg[1] = pygame.image.load("img/koopa_death_L.png")
            koopaX[i] = random.randint(0, 736)
            koopaY[i] = random.randint(20, 150)

        koopa(koopaX[i], koopaY[i], i)




    # fireball movement
    if fireballY <= 0:
        fireballY = 440
        fireball_state = "ready"

    if fireball_state == "fire":
        fire_ball(fireballX, fireballY)
        fireballY -= fireballY_change
        if fireballY == 440:
            fireballImg = pygame.image.load("img/fire/fireball1.png")
        if fireballY == 400:
            fireballImg = pygame.image.load("img/fire/fireball2.png")
        if fireballY == 300:
            fireballImg = pygame.image.load("img/fire/fireball3.png")
        if fireballY == 200:
            fireballImg = pygame.image.load("img/fire/fireball4.png")


    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()