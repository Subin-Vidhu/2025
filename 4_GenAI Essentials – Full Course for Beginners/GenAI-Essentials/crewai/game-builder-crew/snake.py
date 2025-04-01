import pygame
import random

# Initialize the pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Set display dimensions
WIDTH, HEIGHT, BLOCK_SIZE = 600, 400, 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Set clock
clock = pygame.time.Clock()

# Set font for scoring
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def display_score(score):
    value = score_font.render("Score: " + str(score), True, BLACK)
    screen.blit(value, [0, 0])

def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, BLACK, [x[0], x[1], snake_block, snake_block])

def draw_food(food_x, food_y):
    pygame.draw.rect(screen, GREEN, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 6, HEIGHT / 3])

def game_loop():
    game_over = False
    game_close = False

    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    score = 0

    while not game_over:

        while game_close == True:
            screen.fill(BLUE)
            message("You lost! Press C-Continue or Q-Quit", RED)
            display_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != BLOCK_SIZE:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -BLOCK_SIZE:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != BLOCK_SIZE:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -BLOCK_SIZE:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLUE)
        draw_food(food_x, food_y)

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(BLOCK_SIZE, snake_List)
        display_score(score)

        pygame.display.update()

        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            Length_of_snake += 1
            score += 10

        clock.tick(15)

    pygame.quit()

game_loop()