import pygame

from config import WIDTH, HEIGHT, WIDTH2, HEIGHT2, FPS, Colors, MARGIN
from objects import Mob, Finish, Obstacle, create_object_safely

pygame.init()

obstacles = create_object_safely(Obstacle, container=[], count=4)
finishes = create_object_safely(Finish, container=obstacles, count=1)
mob = create_object_safely(Mob, container=obstacles, count=1)

pygame.display.set_caption('Pathfinder')  # Название окна
sc = pygame.display.set_mode((WIDTH, HEIGHT))  # главное окно
clock = pygame.time.Clock()

mob = mob[0]
finish = finishes[0]

moving_forward = False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    #управление мобом
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        mob.angle += mob.rotation_speed
    elif keys[pygame.K_RIGHT]:
        mob.angle -= mob.rotation_speed


    if keys[pygame.K_UP]:
        moving_forward = True
    else:
        moving_forward = False

    # движение вперёд
    if moving_forward:
        mob.rotate(1)



    if keys[pygame.K_DOWN]:
        mob.rotate(-1)

    if mob.x < 0:
        mob.x = 0
    if mob.x > 430:
        mob.x = 430
    if mob.y > 330:
        mob.y = 330
    if mob.y < 0:
        mob.y = 0

    sc.fill(Colors.BLACK)
    surf = pygame.Surface((WIDTH2, HEIGHT2)) # рабочая область
    surf.fill(Colors.BLACK)
    pygame.draw.rect(surf, Colors.WHITE, (0, 0, WIDTH2, HEIGHT2), 2)


    rotated_image = pygame.transform.rotate(mob.get_surface(), mob.angle)
    rotated_rect = rotated_image.get_rect(center=mob.rect().center)
    surf.blit(rotated_image, rotated_rect)



    surf.blit(finish.get_surface(), finish.rect())

    if finish.rect().contains(mob.rect()):
        # finish.x = random.randint(10, 450)
        # finish.y = random.randint(10, 450)
        print('Вы полностью внутри!')

    for start, end in mob.get_rays():
        for obstacle in obstacles:
            if obstacle.rect().clipline(start, end):
                pygame.draw.line(surf, Colors.RED, start, end, 2)
            else:
                pygame.draw.line(surf, Colors.WHITE, start, end, 1)
            result = obstacle.rect().clipline(start, end)
            if result:
                print("Пересечение в точках:", result)

    for obstacle in obstacles:
        surf.blit(obstacle.get_surface(), obstacle.rect())
        if obstacle.rect().contains(mob.rect()):
            print('ПОТРАЧЕНО!')


    sc.blit(surf, (MARGIN, MARGIN))
    pygame.display.update()
    clock.tick(FPS)

