from ctypes import pointer
from math import fabs
import numpy as np
from picar_4wd import *
import time
from enum import Enum
from itertools import groupby
import asciichart as ac

class direction(Enum):
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 240

orient = direction.NORTH

ANGLE_RANGE = 180
STEP = 18
us_step = STEP
current_angle = 0
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2
 
N = 100
pts = np.zeros((N,N))

car_x = int(N/2) 
car_y = int(N/2)

scan_list = []
    

def reading_distance(sensor_angle, dist):
    x = int(dist * np.cos(sensor_angle))
    y = int(dist * np.sin(sensor_angle))
    return x,y

def offset_point(readingX,readingY):
    global car_x,car_y
    if orient == direction.NORTH:
        return car_x + readingX,car_y + readingY
    if orient == direction.SOUTH:
        return car_x + readingX,car_y - readingY
    if orient == direction.EAST:
        return car_x + readingY,car_y - readingX
    if orient == direction.WEST:
        return car_x - readingY,car_y - readingX
    

def append_coords(sensor_angle,dist):
    if dist == -2:
        scan_list.append(False)
        return False
    readingX, readingY = reading_distance(sensor_angle,dist)
    point_x,point_y = offset_point(readingX,readingY)
    if not (point_x < 0 or point_x > N or point_y < 0 or point_y > N):
        scan_list.append((point_x,point_y))
    return point_x,point_y



def make_line(x1,y1,x2,y2):
    if x1 == x2:
        for y in range(min(y1,y2)+1,max(y1,y2)):
            pts[int(y)][int(x1)] = 1
        return
    m =  (y1-y2) / (x1-x2)

    for x in range(min(x1,x2)+1,max(x1,x2)):
        y = m * (x - x1) + y1
        pts[int(y)][int(x)] = 1



def connect_coords():
    #for element in list create pairing for each adjacent element with reading != -2 
    global scan_list
    grouping = [list(g) for k, g in groupby(scan_list, lambda x: x != False) if k]
    for g in grouping:
        if len(g) > 1:
            for i in range(len(g)-1):
                pts[int(g[i][1])][int(g[i][0])] = 1
                pts[int(g[i+1][1])][int(g[i+1][0])] = 1
                make_line(g[i][0],g[i][1],g[i+1][0],g[i+1][1])
        else:
            pts[g[0][1]][g[0][0]] = 1


            

def get_distance_at(angle):
    servo.set_angle(angle)
    time.sleep(0.04)
    distance = us.get_distance()
    return distance

def scan_step():
    global scan_list, current_angle, us_step
    current_angle += us_step
    if current_angle >= max_angle:
        current_angle = max_angle
        us_step = -STEP
    elif current_angle <= min_angle:
        current_angle = min_angle
        us_step = STEP
    dist = get_distance_at(current_angle)
    append_coords(current_angle,dist)
    connect_coords()
    if current_angle == min_angle or current_angle == max_angle:
        if us_step < 0:
            # print("reverse")
            scan_list.reverse()
        # print(scan_list)
        tmp = scan_list.copy()
        scan_list = []
        return tmp
    else:
        return False

for i in range(100):
    scan_step()

for i in pts:
    s = ""
    for j in i:
        if j == 1:
            s += 'x'
        else:
            s += '.'
    print(s)








