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
        self.x = 20
        self.y = 20
        self.radius = 10
        self.diameter = self.radius * 2
        self.speed = 2

        # Создание плоскость нашего моба
        self.surface = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.surface, WHITE, (self.radius, self.radius), self.radius)  # рисуем на плоскости круг

    def get_circle(self):
        return self.surface

    def rect(self):
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
        pygame.draw.rect(self.surface, WHITE, (0, 0, self.width, self.height), self.thickness) #рисуем на плоскости контур, обводящий контур прозрачной Surface

    def get_obstacle(self):
        return self.surface  # Возвращаем уже созданный и залитый Surface

    def rect(self):
        return self.surface.get_rect(topleft=(self.x, self.y)) #создаём rect на плоскости surface, размещая его по координатам

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

    def rect(self):
        return self.surface.get_rect(topleft=(self.x, self.y))

def create_object_safely(cls, container, count):
    objects = []
    for _ in range(count):
        while True:
            obj = cls()
            rect_rect = obj.rect()

            # Проверка границ
            inside_bounds = (rect_rect.left >= 0 and
                             rect_rect.top >= 0 and
                             rect_rect.right <= WIDTH2 and
                             rect_rect.bottom <= HEIGHT2)

            all_items = container + objects
            no_overlap = not any(rect_rect.colliderect(item.rect()) for item in all_items)

            if inside_bounds and no_overlap:
                objects.append(obj)
                break

    return objects

def smob(mob):
    for mob_mob in mob:
        return mob_mob

obstacles = create_object_safely(Obstacle, container=[], count=4)
finishes = create_object_safely(Finish, container=obstacles, count=1)
mob = create_object_safely(Mob, container=obstacles, count=1)

pygame.display.set_caption('Pathfinder')  # Название окна
sc = pygame.display.set_mode((WIDTH, HEIGHT))  # главное окно
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    #Пока ручное управление мобом с ограничением границы рабочей области
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        smob(mob).x -= smob(mob).speed
        if smob(mob).x < 0:
            smob(mob).x = 0
    elif keys[pygame.K_RIGHT]:
        smob(mob).x += smob(mob).speed
        if smob(mob).x > 430:
            smob(mob).x = 430
    elif keys[pygame.K_DOWN]:
        smob(mob).y += smob(mob).speed
        if smob(mob).y > 330:
            smob(mob).y = 330
    elif keys[pygame.K_UP]:
        smob(mob).y -= smob(mob).speed
        if smob(mob).y < 0:
            smob(mob).y = 0

    sc.fill(BLACK)

    MARGIN = 25 #отступ, с которым будет размещена рабочая область на экране
    surf = pygame.Surface((WIDTH2, HEIGHT2)) #рабочая область
    surf.fill(BLACK)

    surf.blit(smob(mob).get_circle(), smob(mob).rect()) #размещаем на плоскости surf плоскость mob. smob(mob).rect() - по каким координатам

    pygame.draw.rect(surf, WHITE, (0, 0, WIDTH2, HEIGHT2), 2) #визуально выделяем рабочую область белым контуром по её границе

    for finish in finishes:
        surf.blit(finish.get_finish(), finish .rect())

        if finish .rect().contains(smob(mob).rect()):
            print('Вы полностью внутри!')

    for obstacle in obstacles:
        surf.blit(obstacle.get_obstacle(), obstacle.rect())

        if obstacle.rect().contains(smob(mob).rect()):
            print('Вы полностью внутри!')

    sc.blit(surf, (MARGIN, MARGIN))
    pygame.display.update()

    clock.tick(FPS)