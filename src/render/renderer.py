import pygame
import random

pygame.init()

FPS = 60 # количество кадров в секунду

# Цвета и их номера
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (197, 227, 27)

WIDTH, HEIGHT = 500, 400  # Размеры главного окна
WIDTH2, HEIGHT2 = 450, 350  # размеры рабочей области


# Класс mob
class Mob:
    def __init__(self):
        self.x = WIDTH2 // 2
        self.y = HEIGHT2 // 2
        self.radius = 10
        self.diameter = self.radius * 2
        self.speed = 2

        # Создание плоскости нашего моба
        self.surface = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.surface, WHITE, (self.radius, self.radius), self.radius)  # рисуем на плоскости круг

    def get_circle(self):
        return self.surface

    def rect_circle(self):
        return self.surface.get_rect(topleft=(self.x, self.y))

# Класс препятствия
class Obstacle:
    def __init__(self):
        self.x = random.randint(10, 450)
        self.y = random.randint(10, 350)
        self.width = random.randint(40, 100)
        self.height = random.randint(40, 100)
        self.thickness = 4

        # Создание плоскости препятствий
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.surface, WHITE, (0, 0, self.width, self.height), self.thickness)

    def get_obstacle(self):
        return self.surface  # Возвращаем уже созданный и залитый Surface

    def rect_obstacle(self):
        return self.surface.get_rect(topleft=(self.x, self.y))


class Finish:
    def __init__(self):
        self.x = random.randint(10, 450)
        self.y = random.randint(10, 350)
        self.width = 25
        self.height = 25

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.set_alpha(100)
        pygame.draw.rect(self.surface, YELLOW, (0, 0, self.width, self.height))

    def get_finish(self):
        return self.surface

    def rect_finish(self):
        return self.surface.get_rect(topleft=(self.x, self.y))


mob = Mob()
obstacles = []  # Список из 5 фигур со случайными координатами
finishes = []

for _ in range(4):
    while True:
        new_obstacle = Obstacle()
        new_rect = new_obstacle.rect_obstacle()

        # Проверка на то, полностью ли внутри рабочей области
        inside_bounds_obs = (new_rect.left >= 0 and
                             new_rect.top >= 0 and
                             new_rect.right <= WIDTH2 and
                             new_rect.bottom <= HEIGHT2)

        # не пересекается ни с одним из существующих
        no_overlap_obs = not any(new_rect.colliderect(obs.rect_obstacle()) for obs in obstacles)

        if inside_bounds_obs and no_overlap_obs:
            obstacles.append(new_obstacle)
            break

for _ in range(1):
    while True:
        finish = Finish()
        rect_finish = finish.rect_finish()

        inside_bounds_fin = (rect_finish.left >= 0 and
                             rect_finish.top >= 0 and
                             rect_finish.right <= WIDTH2 and
                             rect_finish.bottom <= HEIGHT2)

        no_overlap_fin = not any(rect_finish.colliderect(obs.rect_obstacle()) for obs in obstacles)

        if inside_bounds_fin and no_overlap_fin:
            finishes.append(finish)
            break

pygame.display.set_caption('Pathfinder')  # Название окна
sc = pygame.display.set_mode((WIDTH, HEIGHT))  # главное окно
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        mob.x -= mob.speed
        if mob.x < 0:
            mob.x = 0
    elif keys[pygame.K_RIGHT]:
        mob.x += mob.speed
        if mob.x > 430:
            mob.x = 430
    elif keys[pygame.K_DOWN]:
        mob.y += mob.speed
        if mob.y > 330:
            mob.y = 330
    elif keys[pygame.K_UP]:
        mob.y -= mob.speed
        if mob.y < 0:
            mob.y = 0

    sc.fill(BLACK)

    MARGIN = 25
    surf = pygame.Surface((WIDTH2, HEIGHT2))
    surf.fill(BLACK)

    surf.blit(mob.get_circle(), mob.rect_circle())

    pygame.draw.rect(surf, WHITE, (0, 0, WIDTH2, HEIGHT2), 2)

    for fin in finishes:
        surf.blit(fin.get_finish(), fin.rect_finish())

        if fin.rect_finish().contains(mob.rect_circle()):
            print('Вы полностью внутри!')

    for obstacle in obstacles:
        surf.blit(obstacle.get_obstacle(), obstacle.rect_obstacle())

        if obstacle.rect_obstacle().contains(mob.rect_circle()):
            print('Вы полностью внутри!')



    sc.blit(surf, (MARGIN, MARGIN))
    pygame.display.update()

    clock.tick(FPS)