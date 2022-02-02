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


def connect_points(i, j, points=projected_points):
    pygame.draw.line(screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))


scale = 100
circle_pos = [WIDTH / 2, HEIGHT / 2]
point_size = 7
angle = 0

clock = pygame.time.Clock()
while True:
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

    # Update Here
    # For rotation we need to use "Rotation_Matrix"
    # Rotation z axis
    Rotation_Matrix_Z = np.matrix([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
    Rotation_Matrix_X = np.matrix([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]])
    Rotation_Matrix_Y = np.matrix([[np.cos(angle), 0, np.sin(angle)], [0, 1, 0], [-np.sin(angle), 0, np.cos(angle)]])

    angle -= 0.03

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
        pygame.draw.circle(screen, BLACK, (x, y), point_size)
        i += 1

    # draw lines
    connect_points(0, 1)
    connect_points(1, 2)
    connect_points(2, 3)
    connect_points(3, 0)
    connect_points(4, 5)
    connect_points(5, 6)
    connect_points(6, 7)
    connect_points(7, 4)
    connect_points(0, 4)
    connect_points(1, 5)
    connect_points(2, 6)
    connect_points(3, 7)

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
