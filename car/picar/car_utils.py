import sys
from ctypes import pointer
import numpy as np
from math import fabs
import time
from enum import Enum
from itertools import groupby
import picar_4wd as fc
from picar_4wd import Speed
import fileinput
import settings


#general globals,classes,functions-------------------
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



def print_settings():
    print(car_x,car_y)

def print_status():
    #global pts,settings.car_x, settings.car_y, orientation
    print_readable()
    print('location: (', settings.car_x, ',', settings.car_y, ')', '\norientation:', settings.orientation)
    
def print_readable():
    #global pts
    for i in settings.pts:
        s = ""
        for j in i:
            if j == 1:
                s += 'X'
            elif j == 0:
                s += '+'
            elif j == -1:
                s += '-'
                
        print(s)

def set_pos(turn, distance):
    #global orientation,settings.car_x,settings.car_y
    if turn == False:
        if settings.orientation == Orientation.NORTH:
            settings.car_y -= distance
        if settings.orientation == Orientation.EAST:
            settings.car_x += distance
        if settings.orientation == Orientation.SOUTH:
            settings.car_y += distance
        if settings.orientation == Orientation.WEST:
            settings.car_x -= distance
        return
    
    if settings.orientation == Orientation.NORTH:
        if turn == 'Right':
            settings.orientation = Orientation.EAST
        if turn == 'Left':
            settings.orientation = Orientation.WEST
    if settings.orientation == Orientation.EAST:
        if turn == 'Right':
            settings.orientation = Orientation.SOUTH
        if turn == 'Left':
            settings.orientation = Orientation.NORTH
    if settings.orientation == Orientation.SOUTH:
        if turn == 'Right':
            settings.orientation = Orientation.WEST
        if turn == 'Left':
            settings.orientation = Orientation.EAST
    if settings.orientation == Orientation.WEST:
        if turn == 'Right':
            settings.orientation = Orientation.NORTH
        if turn == 'Left':
            settings.orientation = Orientation.SOUTH
    
def test_with_input():
    #global settings.car_x,settings.car_y,orientation
    print("1. Write x of starting point\n2. Write y of starting point\n3. Write x of ending point\n4. Write y of ending point\n5. Write starting orientation of car (N, S, E, W)")
    start = [-1, -1]
    end = [-1, -1]
    count = 0
    #orientation = Orientation.NORTH
    o = 'N'
    for line in fileinput.input():
        if 'q' == line.rstrip():
            break

        if count == 0:
            start[0] = int(line)
            settings.car_x = start[0]
        elif count == 1:
            start[1] = int(line)
            settings.car_y = start[1]
        elif count == 2:
            end[0] = int(line)
        elif count == 3:
            end[1] = int(line)
        elif count == 4:
            o = line
        count += 1
        if count == 5:
            break
    o = o.strip()
    print('!!!', o, '!!!!')
    if o == 'N':
        settings.orientation = Orientation.NORTH
    elif o == 'S':
            settings.orientation = Orientation.SOUTH
    if o == 'E':
        settings.orientation = Orientation.EAST
    if o == 'W':
        settings.orientation = Orientation.WEST
    return tuple(start),tuple(end)

#mapping---------------------------------------



def fill_radius():
    #global settings.car_x,settings.car_y,orientation,pts
    radius = settings.US_THRESHOLD
    for o_x in range(-radius,radius+1):
        o_y = 0
        while(((o_x)**2 + (o_y)**2) < radius**2):
            y = 0
            x = 0
            x,y = offset_point(o_x,o_y)
            if not (y < 0 or y > settings.N-1 or x < 0 or x > settings.N-1):
                settings.pts[y][x] = max(settings.pts[y][x], 0)
            o_y+=1

def reading_distance(sensor_angle, dist):
    x = int(dist * np.sin(sensor_angle * (np.pi / 180)))
    y = int(dist * np.cos(sensor_angle * (np.pi/180)))
    return x,y

def offset_point(readingX,readingY):
    #global settings.car_x,settings.car_y, orientation
    if settings.orientation == Orientation.NORTH:
        return settings.car_x + readingX,settings.car_y - readingY
    if settings.orientation == Orientation.SOUTH:
        return settings.car_x - readingX,settings.car_y + readingY
    if settings.orientation == Orientation.EAST:
        return settings.car_x + readingY,settings.car_y + readingX
    if settings.orientation == Orientation.WEST:
        return settings.car_x - readingY,settings.car_y - readingX

def append_coords(sensor_angle,dist):
    tmp_angle = -sensor_angle
    #global settings.scan_list
    if dist == -2:
        settings.scan_list.append(False)
        return False
    readingX, readingY = reading_distance(tmp_angle,dist)
    point_x,point_y = offset_point(readingX,readingY)
    point_x -= 1
    point_y -= 1
    if not (point_x < 0 or point_x > settings.N-1 or point_y < 0 or point_y > settings.N-1 or dist > settings.US_THRESHOLD):
        settings.scan_list.append((point_x,point_y))
    else:
        settings.scan_list.append(False)
    return point_x,point_y
    
def make_line(x1,y1,x2,y2):
    #global pts
    if x1 == x2:
        for y in range(min(y1,y2)+1,max(y1,y2)):
            settings.pts[int(y)][int(x1)] = 1
        return
    m =  (y2-y1) / (x2-x1)

    for x in range(min(x1,x2)+1,max(x1,x2)):
        y = m * (x - x1) + y1
        settings.pts[int(y)][int(x)] = 1


def connect_coords():
    #for element in list create pairing for each adjacent element with reading != -2 
    #global settings.scan_list, pts
    grouping = [list(g) for k, g in groupby(settings.scan_list, lambda x: x != False) if k]
    #print(grouping)
    
    for g in grouping:
        if len(g) > 1:
            for i in range(len(g)-1):
                settings.pts[int(g[i][1])][int(g[i][0])] = 1
                settings.pts[int(g[i+1][1])][int(g[i+1][0])] = 1
                make_line(g[i][0],g[i][1],g[i+1][0],g[i+1][1])
        else:
            settings.pts[g[0][1]][g[0][0]] = 1

def get_distance_at(angle):
    #print(angle)
    fc.servo.set_angle(angle)
    time.sleep(0.02)
    distance = fc.us.get_distance()
    return distance

def scan_step():
    #global settings.scan_list, settings.current_angle, settings.us_step
    settings.current_angle += settings.us_step
    
    if settings.current_angle >= settings.max_angle:
        settings.current_angle = settings.max_angle
        settings.us_step = -settings.STEP
    elif settings.current_angle <= settings.min_angle:
        settings.current_angle = settings.min_angle
        settings.us_step = settings.STEP
    dist = get_distance_at(settings.current_angle)
    append_coords(settings.current_angle,dist)
    #print(settings.current_angle,dist) 
    if settings.current_angle == settings.min_angle or settings.current_angle == settings.max_angle:
        connect_coords()
        if settings.us_step < 0: 
            # print("reverse")
            settings.scan_list.reverse()
        # print(settings.scan_list)
        tmp = settings.scan_list.copy()
        settings.scan_list = []
        return tmp
    else:
        return False

def single_full_scan():
    #global settings.current_angle, settings.car_x, settings.car_y,orient, pts
    fc.servo.set_angle(settings.min_angle)
    time.sleep(.5)
    settings.current_angle = settings.min_angle
    for i in range(settings.FULL_SCAN):
        scan_step()
    fill_radius()
    
    
#precise movements------------------------

def turn_left90():
    fc.turn_left(10)
    time.sleep(.9)
    fc.stop()
def turn_right90():
    fc.turn_right(10)
    time.sleep(.95)
    fc.stop()
def trav_distance(distance:float, direction):
    m = .5
    speed3 = Speed(4)
    speed4 = Speed(25)
    speed3.start()
    speed4.start()
    if direction == 'forward':
        fc.forward(10)
    elif direction == 'backward':
        fc.backward(10)
    elif direction == 'left':
        fc.turn_left(10)
    elif direction == 'right':
        fc.turn_right(10)
    x = 0
    while (x) < distance * m:
        time.sleep(0.01)
        speed = (speed4() + speed3()) /2
        x += speed * 0.01
        
    print("%scm"%(x/m))
    speed4.deinit()
    speed3.deinit()
    fc.stop()

#obstacle check-----------------------------

def on_board(pos, obstacle_map):
    x = pos[0]
    y = pos[1]

    if x < 0 or x >= len(obstacle_map[0]) or y < 0 or y >= len(obstacle_map):
        return False
   
    return True

def find_forward_dist(obstacle_map, width, orientation, pos):
    x_pos = pos[0]
    y_pos = pos[1]

    forward_counter = sys.maxsize

    if orientation == Orientation.NORTH:
        for x in range(x_pos - int(width / 2), x_pos + int(width / 2) + 1):
            forward_room = 0

            while on_board((x, y_pos - 1 - forward_room), obstacle_map) and obstacle_map[y_pos - 1 - forward_room][x] == 0:
                forward_room += 1
           
            if forward_room < forward_counter:
                forward_counter = forward_room

    if orientation == Orientation.SOUTH:
        for x in range(x_pos - int(width / 2), x_pos + int(width / 2) + 1):
            forward_room = 0

            while on_board((x, y_pos + 1 + forward_room), obstacle_map) and obstacle_map[y_pos + 1 + forward_room][x] == 0:
                forward_room += 1
           
            if forward_room < forward_counter:
                forward_counter = forward_room

    if orientation == Orientation.EAST:
        for y in range(y_pos - int(width / 2), y_pos + int(width / 2) + 1):
            forward_room = 0

            while on_board((x_pos + 1 + forward_room, y), obstacle_map) and obstacle_map[y][x_pos + 1 + forward_room] == 0:
                forward_room += 1
           
            if forward_room < forward_counter:
                forward_counter = forward_room

    if orientation == Orientation.WEST:
        for y in range(y_pos - int(width / 2), y_pos + int(width / 2) + 1):
            forward_room = 0

            while on_board((x_pos - 1 - forward_room, y), obstacle_map) and obstacle_map[y][x_pos - 1 - forward_room] == 0:
                forward_room += 1
           
            if forward_room < forward_counter:
                forward_counter = forward_room

    return forward_counter
