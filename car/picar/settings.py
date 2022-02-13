from sre_parse import CATEGORIES
import numpy as np
from enum import Enum

#general
class Angles(Enum):
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 240
class Orientation(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3
N = 100
pts = np.full((N,N), -1)
car_x = 0
car_y = 0
angle = 0
orientation = Orientation.NORTH
dimensions = (25, 25)
clearance = 2
im_count = 0

#mapping
ANGLE_RANGE = 160
STEP = 10
us_step = STEP
current_angle = 0
max_angle = ANGLE_RANGE/2
min_angle = -(ANGLE_RANGE/2)
US_THRESHOLD = 20
FULL_SCAN = int(ANGLE_RANGE / STEP)
scan_list = []
full_scan_active = False

#printing
output_dir = ''

#detection
detections = []
CATEGORY_LIST = {'stop sign','person', 'traffic light', 'stop light', 'cone', 'traffic cone'}
captures = 0