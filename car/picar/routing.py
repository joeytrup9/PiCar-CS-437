from astar import *
from car_utils import *
import settings
import sys
import printing

def test1():
    turn_left90()
    turn_right90()
if __name__ == "__main__":
    
    #test1()
    #sys.exit()
    #global car_x, car_y, pts,dimensions,clearance,orientation
    #start,end = test_with_input()
    start,end = (150,150),(200,200)
    settings.orientation = Orientation.WEST
    # mark area surrounding car to be free??
    curr_point = start
    settings.car_x = start[0]
    settings.car_y = start[1]
    
    print('start:', start, '\nend:', end, '\nclearance:', settings.clearance, '\norientation:', settings.orientation)
    #print_status()
    #single_full_scan()
    #print_status()
    #sys.exit()
    while ((settings.car_x, settings.car_y) != end):
        
        single_full_scan()
        printing.pretty_printing(settings.pts)
        #print_status()
        path = astar(settings.pts, (settings.car_x, settings.car_y), end, settings.clearance)
        
        print("path: " + str(path))
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
                print(i,d)
                #d = i
                if i > d:
                    trav_distance(d,'forward')
                    set_pos(False, d)
                    break
                else:
                    trav_distance(i,'forward')
                    set_pos(False, i)
            
                    