import numpy as np
import picar_4wd as fc
from follow_path import turn_left90,turn_right90,trav_distance
from astar import *

def follow_path(path):
	for c in path:
		if c == 'Right':
			turn_right90()
		elif c == 'Left':
			turn_left90()
		else:
			trav_distance(c,'forward)
    fc.stop()

if __name__ = '__main__':
    
