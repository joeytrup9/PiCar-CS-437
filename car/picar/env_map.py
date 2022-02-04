import numpy as np
from picar_4wd import *
import time

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

def reading_distance(angle, dist):
    x = dist * np.sin(angle)
    y = dist * np.cos(angle)
    return x,y

def offset_point(readingX,readingY,carX,carY, angle):
    if angle >=0 :
        outX = carX - readingX
    else:
        outX = carX + readingX
    outY = (carY * 2) + readingY
    return outX,outY

def append_coords(angle,dist):
    if dist == -2:
        return False
    global car_x,car_y
    readingX, readingY = reading_distance(angle,dist)
    point_x,point_y = offset_point(readingX,readingY,car_x,car_y,angle)
    if not (point_x < 0 or point_x > N or point_y < 0 or point_y > N):
        pts[point_x][point_y] = 1
    return point_x,point_y

def connect_coords():
    #for element in list create pairing for each adjacent element with reading != -2 
    global scan_list
    tmp = []
    grouping = []
    for r in scan_list:
        if (not r) and tmp != []:
            grouping.append[tmp]
            tmp = []
        elif r != False:
            tmp.append(r)
    for g in grouping:
        for i in range(len(g)):
            
            pass

        

            


def get_distance_at(angle):
    servo.set_angle(angle)
    time.sleep(0.04)
    distance = us.get_distance()
    return angle,distance

def scan_step(ref):
    global scan_list, current_angle, us_step
    current_angle += 18
    if current_angle >= max_angle:
        current_angle = max_angle
        us_step = -STEP
    elif current_angle <= min_angle:
        current_angle = min_angle
        us_step = STEP
    angle,dist = get_distance_at(current_angle)
    pX,pY = append_coords(angle,dist)
    scan_list.append((angle,dist))
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

while 1:
    pass
