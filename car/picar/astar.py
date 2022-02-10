# citation: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2 and
# https://towardsdatascience.com/a-star-a-search-algorithm-eb495fb156bb
import numpy as np
from car_utils import *
from heapq import *
import settings
import copy
def print_readable1(pts):
    for i in np.flipud(pts):
        s = ""
        for j in i:
            if j == 1:
                s += 'X'
            elif j == 2:
                s += 's'
            elif j == 3:
                s += 'd'
            else:
                s += '.'
        print(s)
# citation: https://code.activestate.com/recipes/578919-python-a-pathfinding-with-binary-heap/


# using manhattan distance
def heuristic(node_pos, end_pos):
    return abs(node_pos[0] - end_pos[0]) + abs(node_pos[1] - end_pos[1])


# checks if position is on the board
def on_board(pos, obstacle_map):
    x = pos[0]
    y = pos[1]


    if x < 0 or x >= len(obstacle_map[0]) or y < 0 or y >= len(obstacle_map):
        return False
    
    return True


# gets the path once the end is found
def get_path(start_node, curr_node, previous):
    path = []
    while curr_node in previous:
        path.append(curr_node)
        curr_node = previous[curr_node]


    path.append(start_node)
    return path[::-1]


# checks if position passes given clearance
def passes_clearance(pos, obstacle_map, clearance):
    x = pos[0]
    y = pos[1]


    for y_prime in range(-clearance + y, clearance + y + 1):
        for x_prime in range(-clearance + x, clearance + x + 1):
            if not on_board((x_prime, y_prime), obstacle_map):
                continue


            if obstacle_map[y_prime][x_prime] == 1:
                return False


    return True    


def astar(obstacle_map, start_node, end_node, clearance):
    neighbors = [(0,1),(0,-1),(1,0),(-1,0)]


    close_set = set()
    previous = {}
    g_val = {start_node:0}
    f_val = {start_node:heuristic(start_node, end_node)}
    oheap = []


    heappush(oheap, (f_val[start_node], start_node))
    while oheap:
        curr_node = heappop(oheap)[1]


        # if reached end, return path
        if curr_node == end_node:
            return get_path(start_node, curr_node, previous)


        close_set.add(curr_node)
        for i, j in neighbors:
            neighbor = curr_node[0] + i, curr_node[1] + j            
            tentative_g_score = g_val[curr_node] + heuristic(curr_node, neighbor)


            if on_board(neighbor, obstacle_map):
                # checks if neighbor is obstacle
                if not obstacle_map[neighbor[1]][neighbor[0]] == 1:
                    if neighbor in close_set and tentative_g_score >= g_val.get(neighbor, 0):
                        continue
                
                    if tentative_g_score < g_val.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                        previous[neighbor] = curr_node
                        g_val[neighbor] = tentative_g_score
                        f_val[neighbor] = tentative_g_score + heuristic(neighbor, end_node)


                        if passes_clearance(neighbor, obstacle_map, clearance):
                            heappush(oheap, (f_val[neighbor], neighbor))


    return False


# gets intructions from path
def get_instructions(path):
    #print("inst_path:" + str(path))
    if path == False:
        return False
    
    curr_point = path[0]
    pivot = path[0]
    local_orient = copy.deepcopy(settings.orientation)
    
    instructions = []


    for next_point in path[1:]:
        next_x = next_point[0]
        next_y = next_point[1]


        if local_orient == Orientation.NORTH:
            if next_y == curr_point[1] + 1:
                instructions.append("Right")
                instructions.append("Right")
                local_orient = Orientation.SOUTH
            if next_x == curr_point[0] + 1:
                instructions.append(abs(next_y - pivot[1]))
                instructions.append("Right")
                local_orient = Orientation.EAST
                pivot = curr_point
            elif next_x == curr_point[0] - 1:
                instructions.append(abs(next_y - pivot[1]))
                instructions.append("Left")
                local_orient = Orientation.WEST
                pivot = curr_point


        elif local_orient == Orientation.SOUTH:
            if next_y == curr_point[1] - 1:
                instructions.append("Right")
                instructions.append("Right")
                local_orient = Orientation.NORTH
            if next_x == curr_point[0] - 1:
                instructions.append(abs(next_y - pivot[1]))
                instructions.append("Right")
                local_orient = Orientation.WEST
                pivot = curr_point
            elif next_x == curr_point[0] + 1:
                instructions.append(abs(next_y - pivot[1]))
                instructions.append("Left")
                local_orient = Orientation.EAST
                pivot = curr_point


        elif local_orient == Orientation.EAST:
            if next_x == curr_point[0] - 1:
                instructions.append("Right")
                instructions.append("Right")
                local_orient = Orientation.EAST
            if next_y == curr_point[1] - 1:
                instructions.append(abs(next_x - pivot[0]))
                instructions.append("Left")
                local_orient = Orientation.NORTH
                pivot = curr_point
            elif next_y == curr_point[1] + 1:
                instructions.append(abs(next_x - pivot[0]))
                instructions.append("Right")
                local_orient = Orientation.SOUTH
                pivot = curr_point


        if local_orient == Orientation.WEST:
            if next_x == curr_point[0] + 1:
                instructions.append("Right")
                instructions.append("Right")
                local_orient = Orientation.EAST
            if next_y == curr_point[1] - 1:
                instructions.append(abs(next_x - pivot[0]))
                instructions.append("Right")
                local_orient = Orientation.NORTH
                pivot = curr_point
            elif next_y == curr_point[1] + 1:
                instructions.append(abs(next_x - pivot[0]))
                instructions.append("Left")
                local_orient = Orientation.SOUTH
                pivot = curr_point


        curr_point = next_point


    if local_orient == Orientation.NORTH or local_orient == Orientation.SOUTH:
        instructions.append(abs(curr_point[1] - pivot[1]))


    if local_orient == Orientation.EAST or local_orient == Orientation.WEST:
        instructions.append(abs(curr_point[0] - pivot[0]))


    return instructions

def build_maze():
    maze = []
    graph_size = 100
    for i in range(graph_size):
        tmp = []
        for j in range(graph_size):
            if (j == int(.25 * graph_size) or j == int(.75 * graph_size)) and i > int(.6 * graph_size):
                tmp.append(1)
            elif j == int(.50 * graph_size) and i < int(.4 * graph_size):
                tmp.append(1)
            else:
                tmp.append(0)
        maze.append(tmp)
    return maze

def main():

    maze = build_maze()
    

    start = (5,95)
    end = (95, 5)
    maze[start[1]][start[0]] = 2
    maze[end[1]][end[0]] = 3
    
    print_readable1(maze)
    
    dimensions = (1, 1)
    clearance = 0
    print(clearance)
    path = astar(maze, start, end, clearance)
    print(path)


    print(get_instructions(path, "East"))


    get_instructions(astar(maze, start, end, clearance), local_orient)
    
    # [(0, 8), 'Left', (8, 3)]

def test1():
    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]


    start = (6, 7)
    end = (0, 7)


    dimensions = (2, 2)
    clearance = int(max(dimensions) / 2)
    print(clearance)
    path = astar(maze, start, end, clearance)
    print(path)


    print(get_instructions(path, "East"))


    get_instructions(astar(maze, start, end, clearance), local_orient)
    
if __name__ == '__main__':
    main()
