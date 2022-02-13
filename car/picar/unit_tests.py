from car_utils import *
from printing import *
import settings
from astar import *


def scan_test1():
    settings.car_x, settings.car_y = 50,50
    settings.orientation = Orientation.WEST
    single_full_scan()
    
    settings.car_x, settings.car_y = 250,50
    settings.orientation = Orientation.WEST
    single_full_scan()
    
    settings.car_x, settings.car_y = 50,250
    settings.orientation = Orientation.WEST
    single_full_scan()
    
    settings.car_x, settings.car_y = 250,250
    settings.orientation = Orientation.WEST
    single_full_scan()
    

def scan_test2():
    settings.car_x, settings.car_y = 0,0
    for i in range(5):
        for j in range(5):
            settings.car_x, settings.car_y = i*60+30,j*60+30
            settings.orientation = Orientation.WEST
            single_full_scan()
    

    

if __name__ == '__main__':
    scan_test1()
    #pretty_printing(settings.pts)
    #print_readable()
    