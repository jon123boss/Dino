import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_COLOR = (83, 83, 83)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dinosaur Jump Game")

clock = pygame.time.Clock()
FPS = 30

dino_width = 50
dino_height = 50
dino_x = 50
dino_y = SCREEN_HEIGHT - dino_height - 50
dino_jump = False
jump_height = 10
dino_vel_y = 0

ground_rect = pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)

def draw_ground():
    pygame.draw.rect(screen, GROUND_COLOR, ground_rect)

def draw_dinosaur(x, y):
    pygame.draw.rect(screen, BLACK, (x, y, dino_width, dino_height))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not dino_jump:
                dino_jump = True
                dino_vel_y = -jump_height

    if dino_jump:
        dino_y += dino_vel_y
        dino_vel_y += 1

        if dino_y >= SCREEN_HEIGHT - dino_height - 50:
            dino_y = SCREEN_HEIGHT - dino_height - 50
            dino_jump = False
            dino_vel_y = 0

    screen.fill(WHITE)
    draw_ground()
    draw_dinosaur(dino_x, dino_y)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()