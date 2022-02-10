from astar import *
from car_utils import *


if __name__ == "__main__":
    global car_x, car_y, pts,dimensions,clearance,orientation
    #start,end = test_with_input()
    start,end = (5,5),(5,15)
    orientation = Orientation.SOUTH
    # mark area surrounding car to be free??

    curr_point = start
    
    print('start:', start, '\nend:', end, '\nclearance:', clearance, '\norientation:', orientation)
    print_status()
    while (curr_point != end):
        single_full_scan()
        print_status()
        path = astar(pts, start, end, clearance)
        #print("path: " + str(path))
        instructions = get_instructions(path, orientation)
        #print("instructions: "  + str(instructions))
        
        for i in instructions:
            if i == 'Right':
                turn_right90()
                set_pos(i, 0)
            elif i == 'Left':
                turn_left90()
                set_pos(i, 0)
            else:
                d = find_forward_dist(pts,min(dimensions), orientation,(car_x,car_y))
                if i > d:
                    trav_distance(d,'forward')
                    set_pos(False, d)
                    break
                else:
                    trav_distance(i,'forward')
                    set_pos(False, i)
                
                    