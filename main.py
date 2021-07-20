import pygame
import random
import math
from pygame import mixer

# Iniciar o pygame
pygame.init()

# Resolução do ecrã
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('Images/background.jpg')

# Som do Background
mixer.music.load('Sounds/background.wav')
mixer.music.play(-1)

# Título e Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('Images/icon.png')
pygame.display.set_icon(icon)

# Jogador
playerImg = pygame.image.load('Images/spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Inimigo
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('Images/alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Balas
bulletImg = pygame.image.load('Images/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.5
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

gameover = False


def LerScore():
    try:
        f = open('MaxScore.txt', 'r')
        return int(f.read())
    except:
        return 0


def GravarScore(maxscore):
    anterior = LerScore()
    if maxscore > anterior:
        file = open("MaxScore.txt", "w")
        file.write(str(maxscore))
        file.close()


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_mscore(x, y):
    score = font.render("Record : " + str(LerScore()), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    GravarScore(score_value)


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def IsCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Loop Infinito
running = True
while running:

    # RGB
    screen.fill((200, 255, 255))

    # Background da Imagem
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Esquerda ou Direita tecla pressionada
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('Sounds/laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Não sair das bordas
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Movimento do Inimigo
    if gameover:
        input("teste")

    if not gameover:

        for i in range(num_of_enemies):

            # Game Over
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                    gameover = True
                    game_over_text()
                    break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 0.3
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -0.3
                enemyY[i] += enemyY_change[i]

            # Collision
            collision = IsCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_Sound = mixer.Sound('Sounds/explosion.wav')
                explosion_Sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

    # Movimento da Bala
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY + 40)
    show_mscore(textX, textY)
    pygame.display.update()
