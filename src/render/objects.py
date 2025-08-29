import pygame
import random
from config import BLACK, WHITE, WIDTH, HEIGHT, WIDTH2, HEIGHT2, FPS, YELLOW, COLORS, Colors, MARGIN


class PraOtec:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

# Create child class of PraOtec
class Child(PraOtec):
    def __init__(self):
        super().__init__()
        self.x = 10
        self.y = 10
        self.width = 20
        self.height = 20


# Класс mob
class Mob:
    def __init__(self):
        self.x = 20
        self.y = 20
        self.radius = 10
        self.diameter = self.radius * 2
        self.speed = 2
        self.theta = 0
        # Создание плоскость нашего моба
        self.surface = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.surface, Colors.MOB_COLOR, (self.radius, self.radius), self.radius)  # рисуем на плоскости круг

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

            no_overlap = not any(rect_rect.colliderect(item.rect()) for item in container + objects)

            if inside_bounds and no_overlap:
                objects.append(obj)
                break

    return objects