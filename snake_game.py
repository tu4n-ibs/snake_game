import pygame
import time
import random
import sys
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
BLOCK = 20
FPS = 10
NUM_OBSTACLES = 20  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
GRAY = (80, 80, 80) 

SNAKE_COLORS = [GREEN, BLUE, YELLOW, PURPLE, ORANGE, CYAN]

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game Plus with Obstacles")
clock = pygame.time.Clock()

font = pygame.font.SysFont("comicsansms", 30)
big_font = pygame.font.SysFont("comicsansms", 50)

HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    with open(HIGHSCORE_FILE, 'r') as f:
        try:
            return int(f.read().strip())
        except:
            return 0

def save_highscore(score):
    with open(HIGHSCORE_FILE, 'w') as f:
        f.write(str(score))

def generate_obstacles(snake_positions, food_position):
    obstacles = set()
    max_attempts = 1000
    attempts = 0
    while len(obstacles) < NUM_OBSTACLES and attempts < max_attempts:
        ox = random.randrange(0, WIDTH, BLOCK)
        oy = random.randrange(0, HEIGHT, BLOCK)
        if (ox, oy) not in snake_positions and (ox, oy) != food_position:
            obstacles.add((ox, oy))
        attempts += 1
    return list(obstacles)

def draw_obstacles(obstacles):
    for (ox, oy) in obstacles:
        pygame.draw.rect(win, GRAY, [ox, oy, BLOCK, BLOCK], border_radius=4)

def draw_snake(snake_list, color, direction):
    for i, segment in enumerate(snake_list):
        pygame.draw.rect(win, color, [segment[0], segment[1], BLOCK, BLOCK], border_radius=4)
        if i == len(snake_list) - 1: 
            draw_eyes_and_tongue(segment, direction)

def draw_eyes_and_tongue(head, direction):
    x, y = head
    eye_radius = 3
    tongue_length = 10

    dx, dy = direction

    if dx == 0 and dy == 0:
        eye_pos = [(x + 5, y + 5), (x + BLOCK - 5, y + 5)]
        tongue_start = (x + BLOCK // 2, y)
        tongue_end = (x + BLOCK // 2, y - tongue_length)
    elif dx > 0:
        eye_pos = [(x + BLOCK - 5, y + 5), (x + BLOCK - 5, y + BLOCK - 5)]
        tongue_start = (x + BLOCK, y + BLOCK // 2)
        tongue_end = (x + BLOCK + tongue_length, y + BLOCK // 2)
    elif dx < 0:
        eye_pos = [(x + 5, y + 5), (x + 5, y + BLOCK - 5)]
        tongue_start = (x, y + BLOCK // 2)
        tongue_end = (x - tongue_length, y + BLOCK // 2)
    elif dy > 0:
        eye_pos = [(x + 5, y + BLOCK - 5), (x + BLOCK - 5, y + BLOCK - 5)]
        tongue_start = (x + BLOCK // 2, y + BLOCK)
        tongue_end = (x + BLOCK // 2, y + BLOCK + tongue_length)
    else:
        eye_pos = [(x + 5, y + 5), (x + BLOCK - 5, y + 5)]
        tongue_start = (x + BLOCK // 2, y)
        tongue_end = (x + BLOCK // 2, y - tongue_length)

    for pos in eye_pos:
        pygame.draw.circle(win, BLACK, pos, eye_radius)

    pygame.draw.line(win, RED, tongue_start, tongue_end, 2)

def draw_food(x, y, pulse):
    pygame.draw.circle(win, RED, (int(x + BLOCK / 2), int(y + BLOCK / 2)), int(BLOCK / 2 * (1 + 0.1 * pulse)))

def draw_background_gradient():
    for i in range(HEIGHT):
        r = min(max(200 + i // 6, 0), 255)
        g = min(max(230 - i // 6, 0), 255)
        b = 255
        color = (r, g, b)
        pygame.draw.line(win, color, (0, i), (WIDTH, i))

def message_center(text, color, y_offset=0, size="small"):
    if size == "small":
        mesg = font.render(text, True, color)
    else:
        mesg = big_font.render(text, True, color)
    rect = mesg.get_rect(center=(WIDTH / 2, HEIGHT / 2 + y_offset))
    win.blit(mesg, rect)

def show_score(score, highscore, play_time):
    s = font.render(f"Score: {score}", True, BLACK)
    h = font.render(f"High Score: {highscore}", True, BLACK)
    t = font.render(f"Time: {int(play_time)} s", True, BLACK)
    win.blit(s, [10, 10])
    win.blit(h, [WIDTH - 220, 10])
    win.blit(t, [WIDTH // 2 - 50, 10])

def game_over_screen(score, highscore, play_time):
    win.fill(WHITE)
    message_center("Game Over", RED, -80, size="big")
    message_center(f"Your Score: {score}", BLACK, -30)
    message_center(f"High Score: {highscore}", BLACK, 10)
    message_center(f"Time Played: {int(play_time)} seconds", BLACK, 50)
    message_center("Press R to Restart or Q to Quit", BLUE, 100)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                elif event.key == pygame.K_q:
                    pygame.quit(); sys.exit()

def game_loop():
    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = 0, 0

    snake = []
    length = 1
    score = 0
    color_index = 0

    food_x = round(random.randrange(0, WIDTH - BLOCK) / BLOCK) * BLOCK
    food_y = round(random.randrange(0, HEIGHT - BLOCK) / BLOCK) * BLOCK

    pulse, pulse_dir = 0, 1
    highscore = load_highscore()
    start_time = pygame.time.get_ticks()

    obstacles = generate_obstacles(set(), (food_x, food_y))  
    while True:
        clock.tick(FPS)
        play_time = (pygame.time.get_ticks() - start_time) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -BLOCK, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = BLOCK, 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -BLOCK
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, BLOCK
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]:
                    idx = event.key - pygame.K_1 
                    if 0 <= idx < len(SNAKE_COLORS):
                        color_index = idx

        x += dx
        y += dy

        if (x, y) in obstacles:
            if score > highscore:
                save_highscore(score)
                highscore = score
            game_over_screen(score, highscore, play_time)

        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            if score > highscore:
                save_highscore(score)
                highscore = score
            game_over_screen(score, highscore, play_time)

        draw_background_gradient()

        draw_obstacles(obstacles)

        draw_food(food_x, food_y, pulse)
        pulse += pulse_dir
        if pulse > 5 or pulse < -5:
            pulse_dir *= -1

        snake.append([x, y])
        if len(snake) > length:
            del snake[0]

        for segment in snake[:-1]:
            if segment == [x, y]:
                if score > highscore:
                    save_highscore(score)
                    highscore = score
                game_over_screen(score, highscore, play_time)

        if score != 0 and score % 10 == 0:
            new_color_index = (score // 10) % len(SNAKE_COLORS)
            if new_color_index != color_index:
                color_index = new_color_index

        snake_color = SNAKE_COLORS[color_index % len(SNAKE_COLORS)]
        draw_snake(snake, snake_color, (dx, dy))
        show_score(score, highscore, play_time)
        pygame.display.update()

        if x == food_x and y == food_y:
            length += 1
            score += 1

            snake_positions = set(tuple(pos) for pos in snake)
            possible_positions = [
                (ox, oy) for ox in range(0, WIDTH, BLOCK)
                for oy in range(0, HEIGHT, BLOCK)
                if (ox, oy) not in obstacles and (ox, oy) not in snake_positions
            ]
            if possible_positions:
                food_x, food_y = random.choice(possible_positions)
            else:
                game_over_screen(score, highscore, play_time)

if __name__ == "__main__":
    game_loop()
