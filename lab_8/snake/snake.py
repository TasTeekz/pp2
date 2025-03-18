import pygame
import random
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load background music
pygame.mixer.music.load('./lab_8/snake/song/Still_Woozy_-_Goodie_Bag_73876176.mp3')
pygame.mixer.music.play(-1)

# Game window size
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game Enhanced")
clock = pygame.time.Clock()

# Font setup
font = pygame.font.Font(None, 30)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Snake settings
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_direction = "RIGHT"
change_to = snake_direction
base_speed = 10
level = 1
speed = base_speed + level  # Speed increases with level

# Score
game_score = 0

# Food generation (avoiding snake and walls)
def generate_food():
    while True:
        pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
        if pos not in snake_body:
            return pos

food_pos = generate_food()
food_spawn = True

# Main loop control
isRunning = True

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
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

    # Change direction
    snake_direction = change_to
    if snake_direction == "UP":
        snake_pos[1] -= 10
    elif snake_direction == "DOWN":
        snake_pos[1] += 10
    elif snake_direction == "LEFT":
        snake_pos[0] -= 10
    elif snake_direction == "RIGHT":
        snake_pos[0] += 10

    # Update snake body
    snake_body.insert(0, list(snake_pos))

    # Check if food is eaten
    if snake_pos == food_pos:
        game_score += 1
        food_spawn = False
        # Level up for every 4 points
        if game_score % 4 == 0:
            level += 1
            speed = base_speed + level  # Increase speed with level
    else:
        snake_body.pop()

    # Spawn food in a new valid location
    if not food_spawn:
        food_pos = generate_food()
    food_spawn = True

    # Collision with wall
    if snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
        isRunning = False

    # Collision with itself
    for block in snake_body[1:]:
        if snake_pos == block:
            isRunning = False

    # Draw everything
    screen.fill(BLACK)
    for p in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(p[0], p[1], 10, 10))
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Display score and level
    score_text = font.render(f"Score: {game_score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (20, 20))
    screen.blit(level_text, (20, 50))

    pygame.display.update()
    clock.tick(speed)

# Game Over message
screen.fill(BLACK)
game_over_text = font.render("GAME OVER", True, WHITE)
game_over_rect = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
screen.blit(game_over_text, game_over_rect)
pygame.display.update()
pygame.time.wait(3000)
pygame.quit()
