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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    # Update Here


    screen.fill(WHITE)

    # Draw Stuff Here
    # draw points
    for point in points:
        projected_point = np.dot(Projection_Matrix, point.reshape(3, 1))
        x = int(projected_point[0][0] * scale) + circle_pos[0]
        y = int(projected_point[1][0] * scale) + circle_pos[1]
        pygame.draw.circle(screen, BLACK, (x, y), point_size)

    pygame.display.update()
