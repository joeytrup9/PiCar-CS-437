import numpy as np
from enum import Enum

#general
class Orientation(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3
N = 300
pts = np.full((N,N), -1)
car_x = 0
car_y = 0
angle = 0
orientation = Orientation.NORTH
dimensions = (20, 20)
clearance = 0
im_count = 0

#mapping
ANGLE_RANGE = 160
STEP = 5
us_step = STEP
current_angle = 0
max_angle = ANGLE_RANGE/2
min_angle = -(ANGLE_RANGE/2)
US_THRESHOLD = 20
FULL_SCAN = int(ANGLE_RANGE / STEP)
scan_list = []
