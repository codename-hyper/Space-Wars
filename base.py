import pygame
import random
import math
from pygame import mixer

# pygame initialization
pygame.init()

# screen resolution
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('space.png')

# Title and icon
pygame.display.set_caption('Space wars')
icon_img = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon_img)

# ***   MUSIC   ***

# background music
mixer.music.load('Deep House.wav')
mixer.music.play(-1)

# Bullet Sound
bullet_sound = mixer.Sound('Silencer.wav')

# Explosion Sound
explosion_sound = mixer.Sound('Explosion.wav')

# Bullet ready
# bullet_ready = mixer.Sound('Reload.wav')
# if bullet_state == 'ready':
# bullet_ready.play()

# Gameover Sound
gameover_sound = mixer.Sound('boo.wav')

# Player
player_img = pygame.image.load('spaceshipbig.png')
player_x = 350
player_y = 500
playerchange_x = 0
playerchange_y = 0

# enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemychange_x = []
enemychange_y = []
number_of_enemies = 4
for enemies in range(number_of_enemies):
    enemy_img.append(pygame.image.load('asteroid.png'))
    enemy_x.append(random.randint(0, 800))
    enemy_y.append(-64)
    enemychange_x.append(0)
    enemychange_y.append(1)

# bullet
bullet_img = pygame.image.load('bomb.png')
bullet_x = float()
bullet_y = float()
bulletchange_x = 0
bulletchange_y = 8
bullet_state = 'ready'

# Score
score_value = 0
font_score = pygame.font.Font('freesansbold.ttf', 16)
score_x = 10
score_y = 10


def show_score(x, y):
    score = font_score.render('POINTS : ' + str(score_value), True, (50, 205, 50))
    screen.blit(score, (x, y))


# Gameover
font_gameover = pygame.font.Font('freesansbold.ttf', 64)


def show_gameover():
    gameover = font_gameover.render('GAME OVER', True, (255, 99, 71))
    screen.blit(gameover, (200, 250))


# Player Function
def player(x, y):
    screen.blit(player_img, (x, y))


# Enemy Function
def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


# bullet Function
def bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (bullet_x, bullet_y))


# Collision Function
def collision_bullet(enemy_x, enemy_y, bullet_x, bullet_y):
    Distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if Distance <= 30:
        return True
    else:
        return False


def collision_player(enemy_x, enemy_y, player_x, player_y):
    Distance = math.sqrt((math.pow(enemy_x - player_x, 2)) + (math.pow(enemy_y - player_y, 2)))
    if Distance <= 30:
        return True
    else:
        return False


# check if game is running
running = True
while running:

    # screen colour
    screen.fill((0, 0, 0))

    # Background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerchange_x = -2
            if event.key == pygame.K_RIGHT:
                playerchange_x = 2
            if event.key == pygame.K_UP:
                playerchange_y = -2
            if event.key == pygame.K_DOWN:
                playerchange_y = 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerchange_x = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerchange_y = 0

        # Bullet Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_x = player_x + (playerchange_x + 16)
                    bullet_y = player_y + (playerchange_y + 10)
                    bullet(bullet_x, bullet_y)
                    bullet_sound.play()

    # Player location
    player_x += playerchange_x
    player_y += playerchange_y

    # Enemy Movement
    for i in range(number_of_enemies):
        # enemy Boundry
        if enemy_x[i] <= 0:
            enemy_x[i] = 0
        elif enemy_x[i] >= 736:
            enemy_x[i] = 736

        # Enemy location
        enemy_x[i] += enemychange_x[i]
        enemy_y[i] += enemychange_y[i]

        # Game Over
        if enemy_y[i] >= 600:
            for j in range(number_of_enemies):
                enemy_y[j] = 3000
            show_gameover()
            player_y = 3000
            break

        # Collision
        collided_bullet = collision_bullet(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collided_bullet:
            bullet_y = player_y + (playerchange_y + 10)
            bullet_state = 'ready'
            enemy_x[i] = random.randint(0, 800)
            enemy_y[i] = -64
            score_value += 1
            explosion_sound.play()
        enemy(enemy_x[i], enemy_y[i], i)
        collided_player = collision_player(enemy_x[i], enemy_y[i], player_x, player_y)
        if collided_player:
            for j in range(number_of_enemies):
                enemy_y[j] = 3000
            show_gameover()
            explosion_sound.play()
            gameover_sound.play()
            player_y = 3000
            break
        enemy(enemy_x[i], enemy_y[i], i)
        # Player Boundry
        if collided_player is False and enemy_y[i] < 600:
            if player_x <= 0:
                player_x = 0
            elif player_x >= 736:
                player_x = 736
            if player_y <= 0:
                player_y = 0
            elif player_y >= 536:
                player_y = 536

    # Bullet Movement
    if bullet_state == 'fire':
        bullet(bullet_x, bullet_y)
        bullet_y -= bulletchange_y
    if bullet_y <= 0:
        bullet_state = 'ready'

    player(player_x, player_y)
    show_score(score_x, score_y)
    pygame.display.update()
