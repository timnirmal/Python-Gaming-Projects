# https://en.wikipedia.org/wiki/Isometric_projection#Rotation_angles
# https://en.wikipedia.org/wiki/Rotation_matrix
# https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle

import numpy as np
import pygame

WIDTH, HEIGHT = (800, 600)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.display.set_caption("3D Projection of Cube")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Cube points
points = [np.matrix([-1, -1, 1]), np.matrix([1, -1, 1]), np.matrix([1, 1, 1]), np.matrix([-1, 1, 1]),
          np.matrix([-1, -1, -1]), np.matrix([1, -1, -1]), np.matrix([1, 1, -1]), np.matrix([-1, 1, -1])]

# Now we need multiply this points by the "Projection Matrix"
# This will calculate the position of each 3D point in the 2D screen
Projection_Matrix = np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 0]])

projected_points: list[list[int]] = [
    [n, n] for n in range(len(points))  # This is the list of projected points
]


def connect_points(i, j, points=projected_points, color=BLACK):
    pygame.draw.line(screen, color, (points[i][0], points[i][1]), (points[j][0], points[j][1]))


def connect_lines(a, b, c, d, color=BLUE):
    """
    This Method can be used instead of connect_points and projected_points
    """
    draw_line(a, b, color)
    draw_line(b, c, color)
    draw_line(c, d, color)
    draw_line(d, a, color)


def draw_line(a, b, color=BLUE):
    pygame.draw.line(screen, color, (projected_points[a][0], projected_points[a][1]),
                     (projected_points[b][0], projected_points[b][1]))


def connect_polygon(a, b, c, d, color=RED):
    pygame.draw.polygon(screen, color,
                        (projected_points[a], projected_points[b], projected_points[c], projected_points[d]))


scale = 100
circle_pos = [(WIDTH / 2) - 200, (HEIGHT / 2) + 40]
point_size = 7
angle = 0
angle2 = 90

clock = pygame.time.Clock()


def Draw_Cube(angle, color=BLACK, circle_pos=circle_pos, point_size=point_size, scale=scale):
    # For rotation, we need to use "Rotation_Matrix"
    # Rotation z axis
    Rotation_Matrix_Z = np.matrix([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
    Rotation_Matrix_X = np.matrix([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]])
    Rotation_Matrix_Y = np.matrix([[np.cos(angle), 0, np.sin(angle)], [0, 1, 0], [-np.sin(angle), 0, np.cos(angle)]])

    angle += 0.03

    # Draw Stuff Here
    i = 0
    # draw points
    for point in points:
        # Now before projecting we need calculate the Rotational point by multiplying the point with Rotation Matrix
        Rotated_Point = np.dot(Rotation_Matrix_Z, point.reshape(3, 1))
        Rotated_Point = np.dot(Rotation_Matrix_X, Rotated_Point)
        # Now in drawing each point is dot product with Projection Matrix
        projected_point = np.dot(Projection_Matrix, Rotated_Point)
        x = int(projected_point[0][0] * scale) + circle_pos[0]
        y = int(projected_point[1][0] * scale) + circle_pos[1]
        projected_points[i] = [x, y]
        pygame.draw.circle(screen, color, (x, y), point_size)
        i += 1
    # draw lines
    connect_points(0, 1, color=color)
    connect_points(1, 2, color=color)
    connect_points(2, 3, color=color)
    connect_points(3, 0, color=color)
    connect_points(4, 5, color=color)
    connect_points(5, 6, color=color)
    connect_points(6, 7, color=color)
    connect_points(7, 4, color=color)
    connect_points(0, 4, color=color)
    connect_points(1, 5, color=color)
    connect_points(2, 6, color=color)
    connect_points(3, 7, color=color)

    """Instead of 12 Connect point functions we can use below code
    for p in range(4):
        connect_points(p, (p+1)%4, color=color)
        connect_points(p+4, ((p+1)%4)+4, color=color)
        connect_points(p, (p+4), color=color)
        
    
    """


while True:
    pygame.init()  # now use display and fonts

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    screen.fill(WHITE)

    # Show text
    # font = times new roman
    font = pygame.font.SysFont("comicsansms", 50)
    text = font.render("3D Projection of Cube", True, BLACK)
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    angle += 0.03
    angle2 += 0.03

    # Update Here
    Draw_Cube(angle)
    Draw_Cube(angle2, RED, circle_pos=[circle_pos[0] + 400, circle_pos[1]])

    connect_polygon(0, 1, 2, 3, color=GREEN)
    connect_polygon(4, 5, 6, 7, color=GREEN)
    connect_polygon(0, 4, 7, 3, color=GREEN)
    connect_polygon(1, 5, 6, 2, color=GREEN)
    connect_polygon(0, 1, 5, 4, color=GREEN)
    connect_polygon(2, 6, 7, 3, color=GREEN)

    # connect_lines(0, 1, 2, 3, color=GREEN)
    # connect_lines(4, 5, 6, 7, color=GREEN)
    # connect_lines(0, 4, 7, 3, color=GREEN)
    # connect_lines(1, 5, 6, 2, color=GREEN)
    # connect_lines(0, 1, 5, 4, color=GREEN)
    # connect_lines(2, 6, 7, 3, color=GREEN)

    pygame.display.update()

# Cube Points
# points.append(np.matrix([-1, -1, 1]))
# points.append(np.matrix([1, -1, 1]))
# points.append(np.matrix([1, 1, 1]))
# points.append(np.matrix([-1, 1, 1]))
# points.append(np.matrix([-1, -1, -1]))
# points.append(np.matrix([1, -1, -1]))
# points.append(np.matrix([1, 1, -1]))
# points.append(np.matrix([-1, 1, -1]))
