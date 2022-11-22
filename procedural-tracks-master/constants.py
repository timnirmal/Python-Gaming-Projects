# Screen dimensions
WIDTH = 1500
HEIGHT = 800

###
# Drawing
###
TITLE = 'Procedural Race Track'

STARTING_GRID_TILE = 'static/grid_tile.png'
START_TILE_HEIGHT = 10
START_TILE_WIDTH = 10

# Colors
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RED = [255, 0, 0]
BLUE = [0, 0, 255]
GRASS_GREEN = [58, 156, 53]
GREY = [186, 182, 168]

TRACK_POINT_ANGLE_OFFSET = 3

###
# Track parameters
###

# Boundaries for the numbers of points that will be randomly 
# generated to define the initial polygon used to build the track
MIN_POINTS = 20
MAX_POINTS = 30

SPLINE_POINTS = 1000

# Margin between screen limits and any of the points that shape the
# initial polygon
MARGIN = 120
# minimum distance between points that form the track skeleton
MIN_DISTANCE = 20
# Maximum midpoint displacement for points placed after obtaining the initial polygon
MAX_DISPLACEMENT = 80
# Track difficulty
DIFFICULTY = 0.1
# min distance between two points that are part of thr track skeleton
DISTANCE_BETWEEN_POINTS = 20
# Maximum corner allowed angle
MAX_ANGLE = 120

TRACK_WIDTH = 100

FULL_CORNER_NUM_POINTS = 17


###
# Some seeds I find cool or interesting
###
COOL_TRACK_SEEDS = [
    911, 
    639620465, 
    666574559, 
    689001243, 
    608068482, 
    1546, 
    8, 
    83, 
    945, 
    633, 
    10, 
    23, 
    17, 
    123, 
    1217, 
    12, 
    5644, 
    5562, 
    2317, 
    1964, 
    95894, 
    95521
]
