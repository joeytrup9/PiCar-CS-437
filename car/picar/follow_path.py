import numpy as np 
import picar_4wd as fc
import time
from enum import Enum
from picar_4wd import Speed



def turn_left90():
    fc.turn_left(10)
    time.sleep(1)
    fc.stop()
def turn_right90():
    fc.turn_right(10)
    time.sleep(1)
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


def test_1():
	trav_distance(12.0, 'forward')
	trav_distance(12.0, 'backward')

def test_2():
	trav_distance(30.0, 'left')
	trav_distance(30.0, 'right')
	
if __name__ == "__main__":
    pass
    


	
	
	
