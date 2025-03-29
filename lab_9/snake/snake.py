import pygame
import random
import sys

# Инициализация Pygame и музыки
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('./lab_8/snake/song/Still_Woozy_-_Goodie_Bag_73876176.mp3')
pygame.mixer.music.play(-1)

# Размеры экрана
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game Enhanced")
clock = pygame.time.Clock()

# Цвета и шрифт
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
font = pygame.font.Font(None, 30)

# Змейка
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_direction = "RIGHT"
change_to = snake_direction
base_speed = 10
level = 1
speed = base_speed + level
game_score = 0
grow_segments = 0  # сколько сегментов ещё нужно вырастить

# Еда
food_spawn = False
FOOD_LIFETIME = 5000
current_food = {}

def generate_food():
    while True:
        pos = [random.randrange(1, WIDTH // 10) * 10,
               random.randrange(1, HEIGHT // 10) * 10]
        if pos not in snake_body:
            weight = random.randint(1, 3)
            return {"pos": pos, "weight": weight, "spawn_time": pygame.time.get_ticks()}

# Цикл игры
isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != "DOWN":
                change_to = "UP"
            if event.key == pygame.K_DOWN and snake_direction != "UP":
                change_to = "DOWN"
            if event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                change_to = "LEFT"
            if event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                change_to = "RIGHT"

    # Обновление направления
    snake_direction = change_to
    if snake_direction == "UP":
        snake_pos[1] -= 10
    elif snake_direction == "DOWN":
        snake_pos[1] += 10
    elif snake_direction == "LEFT":
        snake_pos[0] -= 10
    elif snake_direction == "RIGHT":
        snake_pos[0] += 10

    # Добавляем новую голову
    snake_body.insert(0, list(snake_pos))

    # Спавним еду
    if not food_spawn:
        current_food = generate_food()
        food_spawn = True

    # Съедание еды
    if food_spawn and snake_pos == current_food["pos"]:
        food_spawn = False
        grow_segments += current_food["weight"] - 1  # не удалять хвост несколько ходов
        game_score += current_food["weight"]
        if game_score % 4 == 0:
            level += 1
            speed = base_speed + level
        print(f"Съел еду весом {current_food['weight']} — растёт на {current_food['weight']}!")

    else:
        # Проверка на исчезновение еды
        if food_spawn and pygame.time.get_ticks() - current_food["spawn_time"] > FOOD_LIFETIME:
            print("Еда исчезла по таймеру")
            food_spawn = False

        # Удаляем хвост, если не растёт
        if grow_segments > 0:
            grow_segments -= 1
        else:
            snake_body.pop()

    # Столкновение со стеной
    if snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
        print("Выход за границу")
        isRunning = False

    # Столкновение с собой
    if snake_pos in snake_body[1:]:
        print("Столкновение с собой")
        isRunning = False

    # Рисуем всё
    screen.fill(BLACK)
    for block in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], 10, 10))

    if food_spawn:
        pygame.draw.rect(screen, RED, pygame.Rect(current_food["pos"][0], current_food["pos"][1], 10, 10))
        weight_text = font.render(str(current_food["weight"]), True, WHITE)
        screen.blit(weight_text, (current_food["pos"][0], current_food["pos"][1] - 20))

    # Счёт и уровень
    score_text = font.render(f"Score: {game_score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (20, 20))
    screen.blit(level_text, (20, 50))

    pygame.display.update()
    clock.tick(speed)

# Финальный экран
screen.fill(BLACK)
game_over_text = font.render("GAME OVER", True, WHITE)
screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH/2, HEIGHT/2)))
pygame.display.update()
pygame.time.wait(3000)
pygame.quit()
