import pygame
import numpy as np
import math

WHITE = (255, 255, 255)

WIDTH, HEIGHT = (800, 600)

pygame.display.set_caption("3D Projection of Cube")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

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
