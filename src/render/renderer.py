import pygame
import random
from config import BLACK, WHITE, WIDTH, HEIGHT, WIDTH2, HEIGHT2, FPS, YELLOW, COLORS, Colors, MARGIN
from render.objects import Mob, Obstacle, Finish, create_object_safely
pygame.init()




obstacles = create_object_safely(Obstacle, container=[], count=4)
finishes = create_object_safely(Finish, container=obstacles, count=1)
mob = create_object_safely(Mob, container=obstacles, count=1)

pygame.display.set_caption('Pathfinder')  # Название окна
sc = pygame.display.set_mode((WIDTH, HEIGHT))  # главное окно
clock = pygame.time.Clock()

mob = mob[0]
finish = finishes[0]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    #Пока ручное управление мобом с ограничением границы рабочей области
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
    surf = pygame.Surface((WIDTH2, HEIGHT2)) #рабочая область
    surf.fill(BLACK)
    pygame.draw.rect(surf, WHITE, (0, 0, WIDTH2, HEIGHT2), 2) #визуально выделяем рабочую область белым контуром по её границе

    surf.blit(mob.get_circle(), mob.rect()) #размещаем на плоскости surf плоскость mob. smob(mob).rect() - по каким координатам


    for finish in finishes:
        surf.blit(finish.get_finish(), finish.rect())

        if finish.rect().contains(mob.rect()):
            print('Вы полностью внутри!')

    for obstacle in obstacles:
        surf.blit(obstacle.get_obstacle(), obstacle.rect())

        if obstacle.rect().contains(mob.rect()):
            print('ПОТРАЧЕНО!')

    sc.blit(surf, (MARGIN, MARGIN))
    pygame.display.update()


    clock.tick(FPS)