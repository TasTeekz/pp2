import pygame, sys
from pygame.locals import *
import random, time

# Инициализация pygame
pygame.init()

# Настройка FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Определение цветов
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Размеры экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Игровые переменные
SPEED = 5  # начальная скорость врага и монет
SCORE = 0  # счёт за избегание врагов
COINS_COLLECTED = 0  # количество собранных монет
COINS_NEEDED_FOR_SPEEDUP = 10  # ускорение врага каждые N монет

# Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Загрузка фона
background = pygame.image.load("./lab_8/racer/images/AnimatedStreet.png")

# Настройка окна
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer with Coins")

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("./lab_8/racer/images/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        # Если враг уходит за нижнюю границу — добавляется очко и он респавнится сверху
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("./lab_8/racer/images/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # Движение влево
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        # Движение вправо
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# Класс монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./lab_8/racer/images/Coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30))  # масштабируем монету
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        # Задаём новое случайное положение монеты сверху
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.weight = random.randint(1, 3)  # Случайный вес монеты от 1 до 3

    def move(self):
        self.rect.move_ip(0, SPEED - 1)  # монеты двигаются немного медленнее врагов
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()  # если ушла за экран — респавн

# Создание объектов игры
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группы спрайтов
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Отрисовка фона
    DISPLAYSURF.blit(background, (0, 0))

    # Отображение счёта и количества монет
    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
    coin_text = font_small.render("Coins: " + str(COINS_COLLECTED), True, (255, 215, 0))
    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 120, 10))

    # Обновление и отрисовка всех объектов
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Проверка: столкновение игрока с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('./lab_8/racer/images/crash.wav').play()
        time.sleep(0.5)

        # Отображение экрана окончания игры
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()

        # Удаление всех объектов и завершение
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Проверка: сбор монеты игроком
    if pygame.sprite.spritecollideany(P1, coins):
        COINS_COLLECTED += C1.weight  # добавляем вес монеты
        if COINS_COLLECTED % COINS_NEEDED_FOR_SPEEDUP == 0:
            SPEED += 1  # увеличение скорости врагов
        C1.reset_position()  # респавн монеты

    pygame.display.update()
    FramePerSec.tick(FPS)
