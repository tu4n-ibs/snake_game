import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
gray = (100, 100, 100)
yellow = (255, 255, 0)
dark_gray = (40, 40, 40)

width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game by TuanVV")

clock = pygame.time.Clock()
snakeBlock = 10
font = pygame.font.SysFont("bahnschrift", 25)
scoreFont = pygame.font.SysFont("comicsansms", 25)

skins = [
    {"name": "Default Green", "color": (0, 255, 0), "unlock_score": 0},
    {"name": "Deep Blue", "color": (0, 0, 255), "unlock_score": 5},
    {"name": "Bright Red", "color": (255, 0, 0), "unlock_score": 10},
    {"name": "Orange Glow", "color": (255, 165, 0), "unlock_score": 15},
    {"name": "Purple Mist", "color": (128, 0, 128), "unlock_score": 20},
    {"name": "Cyan Breeze", "color": (0, 255, 255), "unlock_score": 25},
    {"name": "Hot Pink", "color": (255, 105, 180), "unlock_score": 30},
    {"name": "Yellow Flash", "color": (255, 255, 0), "unlock_score": 35},
    {"name": "Lime Zest", "color": (50, 205, 50), "unlock_score": 40},
    {"name": "Coral Reef", "color": (255, 127, 80), "unlock_score": 45},
    {"name": "Steel Blue", "color": (70, 130, 180), "unlock_score": 50},
]

current_skin_index = 0
unlocked_skins = {0}

map_scale = 0.1
map_width = int(width * map_scale)
map_height = int(height * map_scale)
map_x = width - map_width - 10
map_y = 10

def load_highscore():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_highscore(highscore):
    with open("highscore.txt", "w") as f:
        f.write(str(highscore))

def draw_score(score):
    value = scoreFont.render(f"Score: {score}", True, white)
    screen.blit(value, [10, 10])

def draw_speed(speed):
    speed_text = scoreFont.render(f"Speed: {speed}", True, white)
    screen.blit(speed_text, [10, 40])

def draw_highscore(highscore):
    highscore_text = scoreFont.render(f"High Score: {highscore}", True, white)
    screen.blit(highscore_text, [10, 70])

def draw_snake(snake_block, snake_list, direction, skin_color):
    for i, pos in enumerate(snake_list):
        pygame.draw.rect(screen, skin_color, [pos[0], pos[1], snake_block, snake_block])
        if i == len(snake_list) - 1:
            x_change, y_change = direction
            eye_radius = 2
            if x_change > 0:
                pygame.draw.circle(screen, black, (pos[0] + snake_block - 3, pos[1] + 3), eye_radius)
                pygame.draw.circle(screen, black, (pos[0] + snake_block - 3, pos[1] + snake_block - 6), eye_radius)
                pygame.draw.rect(screen, red, [pos[0] + snake_block, pos[1] + snake_block // 2 - 1, 5, 2])
            elif x_change < 0:
                pygame.draw.circle(screen, black, (pos[0] + 3, pos[1] + 3), eye_radius)
                pygame.draw.circle(screen, black, (pos[0] + 3, pos[1] + snake_block - 6), eye_radius)
                pygame.draw.rect(screen, red, [pos[0] - 5, pos[1] + snake_block // 2 - 1, 5, 2])
            elif y_change > 0:
                pygame.draw.circle(screen, black, (pos[0] + 3, pos[1] + snake_block - 3), eye_radius)
                pygame.draw.circle(screen, black, (pos[0] + snake_block - 6, pos[1] + snake_block - 3), eye_radius)
                pygame.draw.rect(screen, red, [pos[0] + snake_block // 2 - 1, pos[1] + snake_block, 2, 5])
            elif y_change < 0:
                pygame.draw.circle(screen, black, (pos[0] + 3, pos[1] + 3), eye_radius)
                pygame.draw.circle(screen, black, (pos[0] + snake_block - 6, pos[1] + 3), eye_radius)
                pygame.draw.rect(screen, red, [pos[0] + snake_block // 2 - 1, pos[1] - 5, 2, 5])
            else:
                pygame.draw.circle(screen, black, (pos[0] + snake_block - 3, pos[1] + 3), eye_radius)
                pygame.draw.circle(screen, black, (pos[0] + snake_block - 3, pos[1] + snake_block - 6), eye_radius)
                pygame.draw.rect(screen, red, [pos[0] + snake_block, pos[1] + snake_block // 2 - 1, 5, 2])

def message(msg, color):
    mesg = font.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3])

def generate_obstacles(num=10):
    obstacles = []
    for _ in range(num):
        x = round(random.randrange(0, width - 60) / 10.0) * 10.0
        y = round(random.randrange(0, height - 10) / 10.0) * 10.0
        length = random.choice([30, 40, 50])
        orientation = random.choice(['horizontal', 'vertical'])
        obs_rect = []
        for i in range(length // snakeBlock):
            if orientation == 'horizontal':
                obs_rect.append([x + i * snakeBlock, y])
            else:
                obs_rect.append([x, y + i * snakeBlock])
        obstacles.extend(obs_rect)
    return obstacles

def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(screen, gray, [obs[0], obs[1], snakeBlock, snakeBlock])

def is_position_free(x, y, obstacles):
    for obs in obstacles:
        if x == obs[0] and y == obs[1]:
            return False
    return True

def random_food_position(obstacles):
    while True:
        x = round(random.randrange(0, width - snakeBlock) / 10.0) * 10.0
        y = round(random.randrange(0, height - snakeBlock) / 10.0) * 10.0
        if is_position_free(x, y, obstacles):
            return x, y

def draw_minimap(snake_list, food_pos, big_food_pos, obstacles):
    pygame.draw.rect(screen, dark_gray, (map_x, map_y, map_width, map_height))
    scale = map_scale

    for obs in obstacles:
        mini_x = int(map_x + obs[0] * scale)
        mini_y = int(map_y + obs[1] * scale)
        mini_size = max(1, int(snakeBlock * scale))
        pygame.draw.rect(screen, gray, (mini_x, mini_y, mini_size, mini_size))

    mini_fx = int(map_x + food_pos[0] * scale)
    mini_fy = int(map_y + food_pos[1] * scale)
    mini_size = max(2, int(snakeBlock * scale))
    pygame.draw.circle(screen, yellow, (mini_fx + mini_size // 2, mini_fy + mini_size // 2), mini_size // 2)

    if big_food_pos:
        mini_bx = int(map_x + big_food_pos[0] * scale)
        mini_by = int(map_y + big_food_pos[1] * scale)
        big_size = max(4, int(snakeBlock * scale * 1.5))
        pygame.draw.circle(screen, red, (mini_bx + big_size // 2, mini_by + big_size // 2), big_size // 2)

    skin_color = skins[current_skin_index]["color"]
    for pos in snake_list:
        mini_sx = int(map_x + pos[0] * scale)
        mini_sy = int(map_y + pos[1] * scale)
        mini_size = max(2, int(snakeBlock * scale))
        pygame.draw.rect(screen, skin_color, (mini_sx, mini_sy, mini_size, mini_size))

def gameLoop():
    global current_skin_index, unlocked_skins

    snakeSpeed = 10
    highscore = load_highscore()

    game_over = False
    game_close = False

    x = width / 2
    y = height / 2
    x_change = 0
    y_change = 0

    snake_list = []
    length_of_snake = 1
    score = 0

    obstacles = generate_obstacles()

    foodx, foody = random_food_position(obstacles)
    big_food = None
    big_food_timer = 0

    while not game_over:

        while game_close:
            screen.fill(blue)
            message("Game Over! Press Q-Quit or C-Play Again", red)
            draw_score(score)
            draw_speed(snakeSpeed)
            draw_highscore(highscore)
            pygame.display.update()

            if score > highscore:
                highscore = score
                save_highscore(highscore)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -snakeBlock
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = snakeBlock
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -snakeBlock
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = snakeBlock
                    x_change = 0

                elif event.key == pygame.K_1 and 0 in unlocked_skins:
                    current_skin_index = 0
                elif event.key == pygame.K_2 and 1 in unlocked_skins:
                    current_skin_index = 1
                elif event.key == pygame.K_3 and 2 in unlocked_skins:
                    current_skin_index = 2

        x += x_change
        y += y_change

        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        screen.fill(black)

        pygame.draw.circle(screen, yellow, (int(foodx) + 5, int(foody) + 5), 6)

        if score % 10 == 0 and score != 0 and big_food is None:
            big_food_x, big_food_y = random_food_position(obstacles)
            big_food = [big_food_x, big_food_y]
            big_food_timer = 100

        if big_food:
            pygame.draw.circle(screen, red, (int(big_food[0]) + 5, int(big_food[1]) + 5), 10)
            big_food_timer -= 1
            if big_food_timer <= 0:
                big_food = None

        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        for obs in obstacles:
            if snake_head[0] == obs[0] and snake_head[1] == obs[1]:
                game_close = True

        draw_obstacles(obstacles)

        skin_color = skins[current_skin_index]["color"]
        draw_snake(snakeBlock, snake_list, (x_change, y_change), skin_color)

        draw_score(score)
        draw_speed(snakeSpeed)
        draw_highscore(highscore)

        draw_minimap(snake_list, (foodx, foody), big_food, obstacles)

        for i, skin in enumerate(skins):
            if score >= skin["unlock_score"] and i not in unlocked_skins:
                unlocked_skins.add(i)
                current_skin_index = i

        if x == foodx and y == foody:
            foodx, foody = random_food_position(obstacles)
            length_of_snake += 1
            score += 1
            if score % 5 == 0:
                snakeSpeed += 2

        if big_food and x == big_food[0] and y == big_food[1]:
            big_food = None
            length_of_snake += 3
            score += 3

        pygame.display.update()
        clock.tick(snakeSpeed)

    pygame.quit()
    quit()

gameLoop()