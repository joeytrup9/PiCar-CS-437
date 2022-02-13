from astar import *
from car_utils import *
import settings
import sys
import printing
#import object_detection

def test1():
    print(trav_distance(False, 17))
    turn_left90()
    turn_right90()

def path_and_map(start,end,orientation):
    
    curr_point = start
    settings.car_x = start[0]
    settings.car_y = start[1]
    settings.orientation = orientation
    
    #detector = object_detection.Detector()
    #detector.start()
    
    print('start:', start, '\nend:', end, '\nclearance:', settings.clearance, '\norientation:', settings.orientation)
    
    while ((settings.car_x, settings.car_y) != end):
    
        #if len(settings.detections) > 0:
            #if 'stop sign' in settings.detections:
        #    continue
        single_full_scan()
        
        path = astar(settings.pts, (settings.car_x, settings.car_y), end, settings.clearance)
        # print("path: " + str(path))
        instructions = get_instructions(path)
        
        print("instructions: " + str(instructions))
        if not instructions:
            
            continue
        for i in instructions:
            #k+=1
            # print(k)
            if i == 'Right':
                turn_right90()
                set_pos(i, 0)
            elif i == 'Left':
                turn_left90()
                set_pos(i, 0)
            else:
                d = find_forward_dist(settings.pts,min(settings.dimensions), settings.orientation,(settings.car_x,settings.car_y))
                if d < 6:
                    break
                print("intruction disance = " + str(i))
                print("find_forward_dist disance = " + str(d))
                #print(i,d)
                #d = i
                if i > d:
                    x,obstacle = trav_distance(d,'forward')
                    #set_pos(False, int(round(x)) )  
                    set_pos(False, d)
                    break
                else:
                    x,obstacle = trav_distance(i,'forward')
                    #set_pos(False, int(round(x)))
                    set_pos(False, i)
                    if obstacle:
                        break

def path_and_map2(start,end,orientation):
    
    curr_point = start
    settings.car_x = start[0]
    settings.car_y = start[1]
    settings.orientation = orientation
    
    #detector = object_detection.Detector()
    #detector.start()
    
    print('start:', start, '\nend:', end, '\nclearance:', settings.clearance, '\norientation:', settings.orientation)
    
    while ((settings.car_x, settings.car_y) != end):
        #if len(settings.detections) > 0:
            #if 'stop sign' in settings.detections:
        #    continue
        single_full_scan()
        
        path = astar(settings.pts, (settings.car_x, settings.car_y), end, settings.clearance)
        # print("path: " + str(path))
        instructions = get_instructions(path)
        
        print("instructions: " + str(instructions))
        if not instructions:
            
            continue
        for i in instructions:
            #k+=1
            # print(k)
            if i == 'Right':
                turn_right90()
                set_pos(i, 0)
            elif i == 'Left':
                turn_left90()
                set_pos(i, 0)
            else:
                #print(i,d)
                #d = i
                x,obstacle = trav_distance(i,'forward')
                set_pos(False, round(x))
                #set_pos(False, i)
                if obstacle:
                    break
                
def path_and_map3(start,end,orientation):
    
    curr_point = start
    settings.car_x = start[0]
    settings.car_y = start[1]
    settings.orientation = orientation
    
    print('start:', start, '\nend:', end, '\nclearance:', settings.clearance, '\norientation:', settings.orientation)
    while ((settings.car_x, settings.car_y) != end):
        single_full_scan()
        path = astar(settings.pts, (settings.car_x, settings.car_y), end, settings.clearance)
        print("path: " + str(path))
        instructions = get_instructions(path)
        instructions = limit_instructions(instructions)
        print("instructions: " + str(instructions))
        
        if not instructions:
            continue
        
        for i in range(min(len(instructions), 3)):
            if instructions[i] == 'Right':
                turn_right90()
                set_pos(i, 0)
            elif instructions[i] == 'Left':
                turn_left90()
                set_pos(i, 0)
            else:
                x,obstacle = trav_distance(i,'forward')
                set_pos(False, instructions[i])




if __name__ == "__main__":
    path_and_map3((20,0),(20,90), Orientation.SOUTH)
    #test1()
    sys.exit()
    #global car_x, car_y, pts,dimensions,clearance,orientation
    #start,end = test_with_input()
    start,end = (150,30),(150,270)
    
    # mark area surrounding car to be free??
    curr_point = start
    settings.car_x = start[0]
    settings.car_y = start[1]
    
    #print('start:', start, '\nend:', end, '\nclearance:', settings.clearance, '\norientation:', settings.orientation)
    #print_status()
    #single_full_scan()
    #print_status()
    #sys.exit()
    while ((settings.car_x, settings.car_y) != end):
        
        single_full_scan()
        #printing.pretty_printing(settings.pts)
        #print_status()
        path = astar(settings.pts, (settings.car_x, settings.car_y), end, settings.clearance)
        
        #print("path: " + str(path))
        instructions = get_instructions(path)
        #instructions = [20,'Left', 30, 'Left', 20, 'Left', 30]
        print(instructions)
        #print("instructions: "  + str(instructions))
        if not instructions:
            continue
        for i in instructions:
            if i == 'Right':
                turn_right90()
                set_pos(i, 0)
            elif i == 'Left':
                turn_left90()
                set_pos(i, 0)
            else:
                d = find_forward_dist(settings.pts,min(settings.dimensions), settings.orientation,(settings.car_x,settings.car_y))
                print("intruction disance = " + str(i))
                print("find_forward_dist disance = " + str(d))
                #d = i
                if i > d:
                    x,obstacle = trav_distance(d,'forward')
                    set_pos(False, int(round(x,0)))
                    break
                else:
                    x,obstacle = trav_distance(i,'forward')
                    set_pos(False, int(round(x,0)))
                    if obstacle:
                        break
                    