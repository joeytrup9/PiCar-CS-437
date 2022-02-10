from ctypes import pointer
from math import fabs
import numpy as np
import picar_4wd as fc
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
STEP = 5
us_step = STEP
current_angle = 0
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2
 
N = 50
US_THRESHOLD = 35
pts = np.zeros((N,N))

FULL_SCAN = int(ANGLE_RANGE / STEP) 

car_x = int(N/2)
car_y = int(N/2)

scan_list = []
    


def fill_radius():
    global car_x,car_y,orient
    xc = car_x
    yc = car_y
    radius = US_THRESHOLD
    for o_x in range(-radius,radius+1):
        o_y = 0
        while(((o_x)**2 + (o_y)**2) < radius**2):
            y = 0
            x = 0
            if orient == directions.NORTH:
                y = yc + o_y
                x = xc + o_x
            elif orient == directions.SOUTH:
                y = yc - o_y
                x = xc + o_x
            elif orient == directions.EAST:
                y = yc - o_x
                x = xc + o_y
            elif orient == directions.WEST:
                y = yc - o_x
                x = xc - o_y
            pts[y][x] = max(pts[y][x], 0)
            o_y+=1

def reading_distance(sensor_angle, dist):
    x = int(dist * np.sin(sensor_angle * (np.pi / 180)))
    y = int(dist * np.cos(sensor_angle * (np.pi/180)))
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
    point_x -= 1
    point_y -= 1
    if not (point_x < 0 or point_x > N-1 or point_y < 0 or point_y > N-1 or dist > US_THRESHOLD):
        scan_list.append((point_x,point_y))
    else:
        scan_list.append(False)
    return point_x,point_y



def make_line(x1,y1,x2,y2):
    print(x1,y1,x2,y2)
    if x1 == x2:
        for y in range(min(y1,y2)+1,max(y1,y2)):
            pts[int(y)][int(x1)] = 1
        return
    m =  (y2-y1) / (x2-x1)

    for x in range(min(x1,x2)+1,max(x1,x2)):
        y = m * (x - x1) + y1
        pts[int(y)][int(x)] = 1



def connect_coords():
    #for element in list create pairing for each adjacent element with reading != -2 
    global scan_list
    grouping = [list(g) for k, g in groupby(scan_list, lambda x: x != False) if k]
    print(grouping)
    
    for g in grouping:
        if len(g) > 1:
            for i in range(len(g)-1):
                pts[int(g[i][1])][int(g[i][0])] = 1
                pts[int(g[i+1][1])][int(g[i+1][0])] = 1
                make_line(g[i][0],g[i][1],g[i+1][0],g[i+1][1])
        else:
            pts[g[0][1]][g[0][0]] = 1


            

def get_distance_at(angle):
    print(angle)
    fc.servo.set_angle(angle)
    time.sleep(0.02)
    distance = fc.us.get_distance()
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
    print(current_angle,dist) 
    if current_angle == min_angle or current_angle == max_angle:
        connect_coords()
        if us_step < 0: 
            # print("reverse")
            scan_list.reverse()
        # print(scan_list)
        tmp = scan_list.copy()
        scan_list = []
        return tmp
    else:
        return False



def single_full_scan(x,y, o, g):
    global current_angle, car_x, car_y,orient, pts
    pts = g
    car_x = x
    car_y = y
    orient = o
    fc.servo.set_angle(-90)
    time.sleep(.5)
    current_angle = -90
    for i in range(FULL_SCAN):
        scan_step()
    fill_radius()

def print_readable():
    for i in np.flipud(pts):
        s = ""
        for j in i:
            if j == 1:
                s += 'X'
            elif j == 2:
                s += 'O'
            else:
                s += '.'
        print(s)

def test1():
    single_full_scan()



def test2():
    make_line(0,0,50,50)

test1()
print_readable()
