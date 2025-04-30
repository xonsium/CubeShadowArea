import pygame
import numpy as np
from math import *
from consts import *
from scipy.spatial import ConvexHull
from scipy.spatial._qhull import QhullError

pygame.display.set_caption("Calculate Area of shadow of a Cube")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
font = pygame.font.Font('Iosevka.ttc', 15)

scale = 100

h_len = CUBE_LEN / 2

circle_pos = [WIDTH/4, HEIGHT/2]
area_pos = [3*WIDTH/4, HEIGHT/2]

angle = 0
avg_area = 0
count = 0
points = []

points.append(np.matrix([-h_len, -h_len, h_len]))
points.append(np.matrix([h_len, -h_len, h_len]))
points.append(np.matrix([h_len,  h_len, h_len]))
points.append(np.matrix([-h_len, h_len, h_len]))
points.append(np.matrix([-h_len, -h_len, -h_len]))
points.append(np.matrix([h_len, -h_len, -h_len]))
points.append(np.matrix([h_len, h_len, -h_len]))
points.append(np.matrix([-h_len, h_len, -h_len]))


projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])


projected2d_points = [
    [n, n] for n in range(len(points))
]

projected_points = [
    [n, n] for n in range(len(points))
]


def connect_points(i, j, points):
    pygame.draw.line(
        screen, Color.WHITE, (points[i][0], points[i][1]), (points[j][0], points[j][1]))


clock = pygame.time.Clock()
while True:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    # update stuff

    rotation_z = np.matrix([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1],
    ])

    rotation_y = np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)],
    ])

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)],
    ])
    angle += 0.02

    screen.fill(Color.BG)

    i = 0
    for point in points:
        rotated2d = np.dot(rotation_z, point.reshape((3, 1)))
        rotated2d = np.dot(rotation_y, rotated2d)
        rotated2d = np.dot(rotation_x, rotated2d)

        projected2d = np.dot(projection_matrix, rotated2d)
        a = projected2d[0, 0]
        b = projected2d[1, 0]
        projected2d_points[i] = [a, b]
        

        x = int(projected2d[0, 0] * scale) + circle_pos[0]
        y = int(projected2d[1, 0] * scale) + circle_pos[1]

        projected_points[i] = [x, y]
        pygame.draw.circle(screen, Color.POINT, (x, y), 5)
        i += 1

    try:
        proj_points = np.array(projected2d_points)
        hull = ConvexHull(proj_points)
        hull_points = proj_points[hull.vertices]
        scaled_hull_list = [[int(x * scale + area_pos[0]), int(y * scale + area_pos[1])] for x, y in hull_points]
        shadow_area = hull.volume
        count += 1
        avg_area += (shadow_area - avg_area) / count

        pygame.draw.polygon(screen, Color.SHADOW, scaled_hull_list)

        area_text = font.render(f'Curr Area: {round(shadow_area, 4)}', True, Color.WHITE)
        area_rect = area_text.get_rect()
        area_rect.center = (3*WIDTH/4, 3*HEIGHT/4+50)
        screen.blit(area_text, area_rect)

        avg_area_text = font.render(f'Avg Area: {round(avg_area, 4)}', True, Color.WHITE)
        avg_area_rect = avg_area_text.get_rect()
        avg_area_rect.center = (3*WIDTH/4, 3*HEIGHT/4+70)
        screen.blit(avg_area_text, avg_area_rect)

    except QhullError:
        print(0)

    for p in range(4):
        connect_points(p, (p+1) % 4, projected_points)
        connect_points(p+4, ((p+1) % 4) + 4, projected_points)
        connect_points(p, (p+4), projected_points)


    cube_title = font.render(f'Top View of Cube', True, Color.WHITE)
    area_rect = cube_title.get_rect()
    area_rect.center = (WIDTH/4, HEIGHT/8)
    screen.blit(cube_title, area_rect)

    cube_title = font.render(f'Shape of Shadow', True, Color.WHITE)
    area_rect = cube_title.get_rect()
    area_rect.center = (3*WIDTH/4, HEIGHT/8)
    screen.blit(cube_title, area_rect)

    pygame.display.update()