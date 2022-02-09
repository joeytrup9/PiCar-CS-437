import fileinput
from enum import Enum

class Orientation(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

obstacle_map = [[-1] * 10] * 10
dimensions = (30, 20)
clearance = int(max(dimensions) / 2)

if __name__ == "__main__":
    print("1. Write x of starting point\n2. Write y of starting point\n3. Write x of ending point\n4. Write y of ending point\n5. Write starting orientation of car (N, S, E, W)")
    start = [-1, -1]
    end = [-1, -1]
    orientation = Orientation.NORTH

    count = 0
    for line in fileinput.input():
        if 'q' == line.rstrip():
            break

        if count == 0:
            start[0] = int(line)
        elif count == 1:
            start[1] = int(line)
        elif count == 2:
            end[0] = int(line)
        elif count == 3:
            end[1] = int(line)
        elif count == 4:
            if line == 'N':
                orientation = Orientation.NORTH
            elif line == 'S':
                orientation = Orientation.SOUTH
            if line == 'E':
                orientation = Orientation.EAST
            if line == 'W':
                orientation = Orientation.WEST

        count += 1
        if count == 5:
            break

    start = tuple(start)
    end = tuple(end)

    # mark area surrounding car to be free??

    curr_point = start
    while (curr_point != start):
        # map_area(obstacle_map)
        # get_instructions(astar(obstacle_map, start, end, clearance), orientation)

        pass