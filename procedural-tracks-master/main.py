import argparse
import math
import os
import random as rn
import numpy as np
import pygame
import sys
from pygame.locals import *
from scipy import interpolate
from scipy.spatial import ConvexHull
from constants import *


####
## logical functions
####
def random_points(min=MIN_POINTS, max=MAX_POINTS, margin=MARGIN, min_distance=MIN_DISTANCE):
    pointCount = rn.randrange(min, max + 1, 1)
    points = []
    for i in range(pointCount):
        x = rn.randrange(margin, WIDTH - margin + 1, 1)
        y = rn.randrange(margin, HEIGHT - margin + 1, 1)
        distances = list(
            filter(lambda x: x < min_distance, [math.sqrt((p[0] - x) ** 2 + (p[1] - y) ** 2) for p in points]))
        if len(distances) == 0:
            points.append((x, y))
    return np.array(points)


def get_track_points(hull, points):
    # get the original points from the random 
    # set that will be used as the track starting shape
    return np.array([points[hull.vertices[i]] for i in range(len(hull.vertices))])


def make_rand_vector(dims):
    vec = [rn.gauss(0, 1) for i in range(dims)]
    mag = sum(x ** 2 for x in vec) ** .5
    return [x / mag for x in vec]


def shape_track(track_points, difficulty=DIFFICULTY, max_displacement=MAX_DISPLACEMENT, margin=MARGIN):
    track_set = [[0, 0] for i in range(len(track_points) * 2)]
    for i in range(len(track_points)):
        displacement = math.pow(rn.random(), difficulty) * max_displacement
        disp = [displacement * i for i in make_rand_vector(2)]
        track_set[i * 2] = track_points[i]
        track_set[i * 2 + 1][0] = int((track_points[i][0] + track_points[(i + 1) % len(track_points)][0]) / 2 + disp[0])
        track_set[i * 2 + 1][1] = int((track_points[i][1] + track_points[(i + 1) % len(track_points)][1]) / 2 + disp[1])
    for i in range(3):
        track_set = fix_angles(track_set)
        track_set = push_points_apart(track_set)
    # push any point outside screen limits back again
    final_set = []
    for point in track_set:
        if point[0] < margin:
            point[0] = margin
        elif point[0] > (WIDTH - margin):
            point[0] = WIDTH - margin
        if point[1] < margin:
            point[1] = margin
        elif point[1] > HEIGHT - margin:
            point[1] = HEIGHT - margin
        final_set.append(point)
    return final_set


def push_points_apart(points, distance=DISTANCE_BETWEEN_POINTS):
    # distance might need some tweaking
    distance2 = distance * distance
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p_distance = math.sqrt((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2)
            if p_distance < distance:
                dx = points[j][0] - points[i][0];
                dy = points[j][1] - points[i][1];
                dl = math.sqrt(dx * dx + dy * dy);
                dx /= dl;
                dy /= dl;
                dif = distance - dl;
                dx *= dif;
                dy *= dif;
                points[j][0] = int(points[j][0] + dx);
                points[j][1] = int(points[j][1] + dy);
                points[i][0] = int(points[i][0] - dx);
                points[i][1] = int(points[i][1] - dy);
    return points


def fix_angles(points, max_angle=MAX_ANGLE):
    for i in range(len(points)):
        if i > 0:
            prev_point = i - 1
        else:
            prev_point = len(points) - 1
        next_point = (i + 1) % len(points)
        px = points[i][0] - points[prev_point][0]
        py = points[i][1] - points[prev_point][1]
        pl = math.sqrt(px * px + py * py)
        px /= pl
        py /= pl
        nx = -(points[i][0] - points[next_point][0])
        ny = -(points[i][1] - points[next_point][1])
        nl = math.sqrt(nx * nx + ny * ny)
        nx /= nl
        ny /= nl
        a = math.atan2(px * ny - py * nx, px * nx + py * ny)
        if (abs(math.degrees(a)) <= max_angle):
            continue
        diff = math.radians(max_angle * math.copysign(1, a)) - a
        c = math.cos(diff)
        s = math.sin(diff)
        new_x = (nx * c - ny * s) * nl
        new_y = (nx * s + ny * c) * nl
        points[next_point][0] = int(points[i][0] + new_x)
        points[next_point][1] = int(points[i][1] + new_y)
    return points



def smooth_track(track_points):
    x = np.array([p[0] for p in track_points])
    y = np.array([p[1] for p in track_points])

    # append the starting x,y coordinates
    x = np.r_[x, x[0]]
    y = np.r_[y, y[0]]

    # fit splines to x=f(u) and y=g(u), treating both as periodic. also note that s=0
    # is needed in order to force the spline fit to pass through all the input points.
    tck, u = interpolate.splprep([x, y], s=0, per=True)

    # evaluate the spline fits for # points evenly spaced distance values
    xi, yi = interpolate.splev(np.linspace(0, 1, SPLINE_POINTS), tck)
    return [(int(xi[i]), int(yi[i])) for i in range(len(xi))]



def find_closest_point(points, keypoint):
    min_dist = None
    closest_point = None
    for p in points:
        dist = math.hypot(p[0] - keypoint[0], p[1] - keypoint[1])
        if min_dist is None or dist < min_dist:
            min_dist = dist
            closest_point = p
    return closest_point


####
## drawing functions
####
def draw_track(surface, color, points):
    radius = TRACK_WIDTH // 2
    # draw track
    chunk_dimensions = (radius * 2, radius * 2)
    for point in points:
        blit_pos = (point[0] - radius, point[1] - radius)
        track_chunk = pygame.Surface(chunk_dimensions, pygame.SRCALPHA)
        pygame.draw.circle(track_chunk, color, (radius, radius), radius)
        surface.blit(track_chunk, blit_pos)
    starting_grid = draw_starting_grid(radius * 2)
    # rotate and place starting grid
    offset = TRACK_POINT_ANGLE_OFFSET
    vec_p = [points[offset][1] - points[0][1], -(points[offset][0] - points[0][0])]
    n_vec_p = [vec_p[0] / math.hypot(vec_p[0], vec_p[1]), vec_p[1] / math.hypot(vec_p[0], vec_p[1])]
    # compute angle
    angle = math.degrees(math.atan2(n_vec_p[1], n_vec_p[0]))
    rot_grid = pygame.transform.rotate(starting_grid, -angle)
    start_pos = (points[0][0] - math.copysign(1, n_vec_p[0]) * n_vec_p[0] * radius,
                 points[0][1] - math.copysign(1, n_vec_p[1]) * n_vec_p[1] * radius)
    start_pos = (700,650)
    # draw circle on start position
    #pygame.draw.circle(surface, (0,0,0), (int(start_pos[0]), int(start_pos[1])), 10)
    print(start_pos)
    surface.blit(rot_grid, start_pos)


def draw_starting_grid(track_width):
    tile_height = START_TILE_HEIGHT  # Move outside
    tile_width = START_TILE_WIDTH  # Move outside
    grid_tile = pygame.image.load(STARTING_GRID_TILE)
    starting_grid = pygame.Surface((track_width, tile_height), pygame.SRCALPHA)
    for i in range(track_width // tile_height):
        position = (i * tile_width, 0)
        starting_grid.blit(grid_tile, position)
    return starting_grid


####
## Main function
####
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # background_color = GRASS_GREEN
    background_color = WHITE
    screen.fill(background_color)

    # generate the track
    points = random_points()
    hull = ConvexHull(points)
    track_points = shape_track(get_track_points(hull, points))
    f_points = smooth_track(track_points)
    # get complete corners from key points
    # draw the actual track (road, kerbs, starting grid)
    draw_track(screen, GREY, f_points)

    pygame.display.set_caption(TITLE)
    while True:  # main loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        # save the image
        pygame.image.save(screen, "track.png")


if __name__ == '__main__':
    # rn.seed(rn.choice(COOL_TRACK_SEEDS))
    main()

