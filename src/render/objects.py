import pygame
import random
from config import WIDTH, HEIGHT, WIDTH2, HEIGHT2, FPS, Colors, MARGIN

class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA) # Создание плоскости для объекта

    def get_surface(self):
        return self.surface # Возвращаем уже созданный и залитый

    def rect(self):
        return self.surface.get_rect(topleft=(self.x, self.y))

class Mob(Rect):
    def __init__(self):
        self.radius = 10
        diameter = self.radius * 2
        x, y = 20, 20
        super().__init__(x, y, diameter, diameter)
        self.speed = 1.5
        self.theta = 0
        self.angle = 0
        self.rotation_speed = 4
        self.ray_length = 120
        pygame.draw.circle(self.surface, Colors.MOB_COLOR, (self.radius, self.radius), self.radius)

        pygame.draw.line(self.surface, Colors.BLACK, (self.radius, self.radius), (20,10), 2)


    def rotate(self, direction):
        # direction = 1 - вперёд
        # direction = -1 - назад
        # вектор направления по углу
        vector = pygame.math.Vector2(1, 0).rotate(-self.angle)
        self.x += vector.x * self.speed * direction
        self.y += vector.y * self.speed * direction

    def get_rays(self):
        center = pygame.math.Vector2(self.x + self.radius, self.y + self.radius)

        rays = []
        for offset in [0, -30, 30]:  # прямо, влево и вправо
            direction = pygame.math.Vector2(1, 0).rotate(-(self.angle + offset))
            end = center + direction * self.ray_length
            rays.append((center, end))
        return rays

class Obstacle(Rect):
    def __init__(self):
        width = random.randint(40, 100)
        height = random.randint(40, 100)
        x = random.randint(10, 450)
        y = random.randint(10, 350)
        super().__init__(x, y, width, height)
        self.thickness = 4
        pygame.draw.rect(self.surface, Colors.WHITE, (0, 0, self.width, self.height), self.thickness)



class Finish(Rect):
    def __init__(self):
        width, height = 25, 25
        x = random.randint(10, 450)
        y = random.randint(10, 350)
        super().__init__(x, y, width, height)
        self.surface.set_alpha(100)
        pygame.draw.rect(self.surface, Colors.YELLOW, (0, 0, self.width, self.height))



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
