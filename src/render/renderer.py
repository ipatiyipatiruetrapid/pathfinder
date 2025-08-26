import pygame
import random

pygame.init()

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WIDTH, HEIGHT = 500, 400


class Obstacle:
    def __init__(self):
        self.x = random.randint(10, 490)
        self.y = random.randint(10, 390)
        self.width = random.randint(40, 100)
        self.height = random.randint(40, 100)
        # Создаём Surface один раз
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(WHITE)  # Заполняем белым сразу

    def draw(self):
        return self.surface  # Возвращаем уже созданный и залитый Surface

    def rect(self):
        return self.surface.get_rect(topleft=(self.x, self.y))


obstacles = [Obstacle() for _ in range(5)]

pygame.display.set_caption('Pathfinder')
sc = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

x = WIDTH // 2
y = HEIGHT // 2
speed = 2

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= speed
    elif keys[pygame.K_RIGHT]:
        x += speed
    elif keys[pygame.K_DOWN]:
        y += speed
    elif keys[pygame.K_UP]:
        y -= speed

    sc.fill(BLACK)

    MARGIN = 25
    surf = pygame.Surface((450, 350))
    surf.fill(BLACK)

    pygame.draw.circle(surf, WHITE, (x, y), 10)

    pygame.draw.rect(surf, WHITE, (0, 0, 450, 350), 2)

    for obstacle in obstacles:
        surf.blit(obstacle.draw(), (obstacle.x, obstacle.y))

    sc.blit(surf, (MARGIN, MARGIN))
    pygame.display.update()

    clock.tick(FPS)