import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_COLOR = (83, 83, 83)
DINO_COLOR = (0, 153, 76)
CACTUS_COLORS = [(255, 0, 0), (0, 0, 255), (255, 165, 0)]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dinosaur Jump Game")

clock = pygame.time.Clock()
FPS = 60

dino_width = 50
dino_height = 50
dino_x = 50
dino_y = SCREEN_HEIGHT - dino_height - 50
dino_jump = False
jump_velocity = 15
gravity = 1
dino_vel_y = 0

ground_rect = pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)

obstacle_min_gap = 200
obstacle_max_gap = 400
obstacle_speed = 5
obstacle_list = []

class Obstacle:
    def __init__(self, x, obstacle_type):
        self.x = x
        self.obstacle_type = obstacle_type
        self.color = CACTUS_COLORS[random.randint(0, len(CACTUS_COLORS) - 1)]
        if obstacle_type == 1:
            self.width = 20
            self.height = 40
        elif obstacle_type == 2:
            self.width = 30
            self.height = 30
        elif obstacle_type == 3:
            self.width = 15
            self.height = 50
        self.y = SCREEN_HEIGHT - self.height - 50

    def move(self):
        self.x -= obstacle_speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def off_screen(self):
        return self.x < -self.width

def draw_ground():
    pygame.draw.rect(screen, GROUND_COLOR, ground_rect)

def draw_dinosaur(x, y):
    pygame.draw.rect(screen, DINO_COLOR, (x, y, dino_width, dino_height))

def check_collision(dino_rect, obstacle_rect):
    return dino_rect.colliderect(obstacle_rect)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

running = True
obstacle_timer = 0
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not dino_jump:
                dino_jump = True
                dino_vel_y = -jump_velocity
            if event.key == pygame.K_r and game_over:

                dino_y = SCREEN_HEIGHT - dino_height - 50
                dino_jump = False
                dino_vel_y = 0
                obstacle_list.clear()
                obstacle_timer = 0
                game_over = False

    if dino_jump:
        dino_y += dino_vel_y
        dino_vel_y += gravity

        if dino_y >= SCREEN_HEIGHT - dino_height - 50:
            dino_y = SCREEN_HEIGHT - dino_height - 50
            dino_jump = False
            dino_vel_y = 0

    if obstacle_timer == 0:
        obstacle_type = random.randint(1, 3)
        obstacle_list.append(Obstacle(SCREEN_WIDTH, obstacle_type))
        obstacle_timer = random.randint(obstacle_min_gap, obstacle_max_gap)
    else:
        obstacle_timer -= 1

    for obstacle in obstacle_list[:]:
        obstacle.move()
        if obstacle.off_screen():
            obstacle_list.remove(obstacle)

    dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
    for obstacle in obstacle_list:
        obstacle_rect = pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
        if check_collision(dino_rect, obstacle_rect):
            game_over = True
            break

    screen.fill(WHITE)
    draw_ground()
    draw_dinosaur(dino_x, dino_y)
    for obstacle in obstacle_list:
        obstacle.draw()

    if game_over:

        font = pygame.font.Font(None, 36)
        draw_text("Game Over", font, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("Press 'r' to restart", font, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()