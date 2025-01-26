import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("Background.png")

# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("Spaceship.png")
pygame.display.set_icon(icon)

# Player 370 480
playerImg = pygame.image.load("Fighter.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy random movement
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("Alien.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(40) # calculates the pixel travelled by enemy

# Bullet movement
# Ready = You can't see the bullet on screen
# Fire = The bullet is currently moving
bulletImg = pygame.image.load("Bullet.png")
bulletX = 0
bulletY = 480  # player y's position
bulletX_change = 0
bulletY_change = 20  # this will calculate the speed
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX =10
textY =10

#Game over text:
over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score = font.render("Score : " + str(score_value),True, (255,255,255))
    screen.blit(score ,(x,y))

def game_over_text():
    over_text = over_font.render(" GAME OVER ",True, (255,255,255))
    screen.blit(over_text ,(200,250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y , i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    # RGB values are printed on the screen 0 to 255
    screen.fill((0, 0, 0))

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -10
            if event.key == pygame.K_RIGHT:
                playerX_change = 10
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # get the current x-coordinate of spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1
    # change of value for playerX
    playerX += playerX_change
    # Adding boundaries for player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # 800-64
        playerX = 736

    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        # change of value for enemyX (enemy movements)
        enemyX[i] += enemyX_change[i]
        # Adding boundaries for enemy
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  # 800-64
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            #increase difficulty:
            # If remainder is 0 it means that score_value is a multiple of 5
            if score_value % 5 == 0:
                for j in range(num_of_enemies):
                    if enemyX_change[j] > 0:
                        enemyX_change[j] += 1
                    else:
                        enemyX_change[j] -= 1

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        # enemy function we defined above
        enemy(enemyX[i], enemyY[i], i)


    # Bullet Movement:
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    # player function we defined above
    player(playerX, playerY)

    #score:
    show_score(textX,textY)

    # update display (end of every game)
    pygame.display.update()
