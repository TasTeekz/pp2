import pygame, sys
from pygame.locals import *
import random, time

# Initializing pygame
pygame.init()

# Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

# Defining colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Game variables
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0

# Setting up fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load background
background = pygame.image.load("./lab_8/racer/images/AnimatedStreet.png")

# Setup display
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer with Coins")

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("./lab_8/racer/images/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("./lab_8/racer/images/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./lab_8/racer/images/Coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED - 1)  # Coins move slightly slower
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()

    def reset_position(self):
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Instantiate player, enemy, and coin
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Create sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Speed increase event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    DISPLAYSURF.blit(background, (0, 0))

    # Display score and coin count
    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
    coin_text = font_small.render("Coins: " + str(COINS_COLLECTED), True, (255, 215, 0))
    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 120, 10))

    # Update and draw all sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Collision: Player hits Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('./lab_8/racer/images/crash.wav').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()

        for entity in all_sprites:
            entity.kill()

        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Collision: Player collects Coin
    if pygame.sprite.spritecollideany(P1, coins):
        COINS_COLLECTED += 1
        C1.reset_position()

    pygame.display.update()
    FramePerSec.tick(FPS)