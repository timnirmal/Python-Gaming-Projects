import numpy as np
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = (800, 600)

pygame.display.set_caption("3D Projection of Cube")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Cube points
points = [np.matrix([-1, -1, 1]), np.matrix([1, -1, 1]), np.matrix([1, 1, 1]), np.matrix([-1, 1, 1]),
          np.matrix([-1, -1, -1]), np.matrix([1, -1, -1]), np.matrix([1, 1, -1]), np.matrix([-1, 1, -1])]

# points.append(np.matrix([-1, -1, 1]))
# points.append(np.matrix([1, -1, 1]))
# points.append(np.matrix([1, 1, 1]))
# points.append(np.matrix([-1, 1, 1]))
# points.append(np.matrix([-1, -1, -1]))
# points.append(np.matrix([1, -1, -1]))
# points.append(np.matrix([1, 1, -1]))
# points.append(np.matrix([-1, 1, -1]))

# Now we need multiply this points by the "Projection Matrix"
Projection_Matrix = np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 0]])

# Now in drawing each point is dot product with Projection Matrix

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

    # Update Here
    # For rotation we need to use "Rotation_Matrix"
    # Rotation z axis
    Rotation_Matrix_Z = np.matrix([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
    Rotation_Matrix_X = np.matrix([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]])
    Rotation_Matrix_Y = np.matrix([[np.cos(angle), 0, np.sin(angle)], [0, 1, 0], [-np.sin(angle), 0, np.cos(angle)]])

    angle += 0.05


    screen.fill(WHITE)

    # Draw Stuff Here
    # draw points
    for point in points:
        # Now before projecting we need calculate the Rotational point by multiplying the point with Rotation Matrix
        Rotated_Point = np.dot(Rotation_Matrix_Z, point.reshape(3, 1))
        Rotated_Point = np.dot(Rotation_Matrix_X, Rotated_Point)
        projected_point = np.dot(Projection_Matrix, Rotated_Point)
        x = int(projected_point[0][0] * scale) + circle_pos[0]
        y = int(projected_point[1][0] * scale) + circle_pos[1]
        pygame.draw.circle(screen, BLACK, (x, y), point_size)

    pygame.display.update()
