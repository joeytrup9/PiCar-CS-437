from astar import *
from car_utils import *
import settings
import sys
import printing
import time
import signal
from settings import Orientation
from picar_4wd import Speed

def handler(sig,frame):
    fc.stop()
    sys.exit()
def scan_and_travel(distance:int,direction): 
    print(distance)
    m = .5
    speed3 = Speed(4)
    speed4 = Speed(25)
    speed3.start()
    speed4.start()
    x = 0
    obstacle = False
    if direction == 1: #forward
        fc.forward(2)
    elif direction == -1: #backward (for testing)
        fc.backward(3)
    while x < distance:
        stime = time.time()
        scans = fc.scan_step(25)
        #print(scans)
        if scans and len(scans) > 5 and scans[3:7] != [2,2,2,2]:
            fc.stop()
            obstacle = True
            break
        etime = time.time()
        speed = (speed4() + speed3()) /2
        x += speed * (etime-stime)
    
    fc.stop()
    fc.scan_list = []
    fc.current_angle = 0
    speed3.deinit()
    speed4.deinit()
    print(x, 'cm')
    return x, obstacle
        
def mark_end(end):
    for i in range(end[0] - 3, end[0] + 4):
        for j in range(end[1] - 3, end[1] + 4):
            settings.pts[j][i] = -2

def alternate_routing(start,end,orientation):
    signal.signal(signal.SIGINT,handler)
    mark_end(end)
    settings.car_x,settings.car_y,settings.orientation = start[0],start[1],orientation
    print(settings.car_x,settings.car_y,settings.orientation)
    single_full_scan()
    while not (settings.car_x > end[0] - 3 and settings.car_y > end [1]- 3 and settings.car_x < end[0] + 3 and settings.car_y < end[1] + 3):
        print((settings.car_x,settings.car_y),settings.orientation)
        path = astar(settings.pts, (settings.car_x, settings.car_y), end, settings.clearance)
        instructions = get_instructions(path)
        if not instructions:
            print('cant move!')
            x,o = scan_and_travel(4,-1)
            set_pos(False,-round(x))
            printing.pretty_printing(settings.pts)
            continue
        for i in instructions:
            if i == 0:
                i+=1
            if i == 'Left':
                turn_left90()
                set_pos(i,0)
            elif i == 'Right':
                turn_right90()
                set_pos(i,0)
            else:
                x,o = scan_and_travel(i,1)
                set_pos(False,round(x))
                printing.pretty_printing(settings.pts)
                if o:
                    single_full_scan()
                    break
    
    print("made it fools!")


def tuning():
    #print(scan_and_travel(100,1))
    #print(scan_and_travel(10*2.54,-1))
    turn_left90()
    time.sleep(2)
    turn_right90()

if __name__ == '__main__':
    #tuning()
    #sys.exit()
    alternate_routing((15,15),(30,70),Orientation.SOUTH)