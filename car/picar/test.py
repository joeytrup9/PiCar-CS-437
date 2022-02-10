# citation: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2 and
# https://towardsdatascience.com/a-star-a-search-algorithm-eb495fb156bb
from car_utils import Orientation

orientation = Orientation.NORTH
class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position


        self.g = 0
        self.h = 0
        self.f = 0


    def __eq__(self, other):
        return self.position == other.position


def get_path(node):
    path = []
    
    while node is not None:
        path.append(node.position)
        node = node.parent


    path = path[::-1]
    return path


def on_board(pos, obstacle_map):
    x = pos[0]
    y = pos[1]


    if x < 0 or x >= len(obstacle_map[0]) or y < 0 or y >= len(obstacle_map):
        return False
    
    return True


def is_valid(pos, obstacle_map):
    if not on_board(pos, obstacle_map):
        return False
    
    x = pos[0]
    y = pos[1]


    if obstacle_map[y][x] == 1:
        return False


    return True


def get_neighbors_pos(pos, obstacle_map):
    neighbors = []
    x = pos[0]
    y = pos[1]


    north, south, east, west = (x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)


    if is_valid(north, obstacle_map):
        neighbors.append(north)
    if is_valid(south, obstacle_map):
        neighbors.append(south)
    if is_valid(east, obstacle_map):
        neighbors.append(east)
    if is_valid(west, obstacle_map):
        neighbors.append(west)


    return neighbors


def heuristic(node_pos, end_pos):
    return abs(node_pos[0] - end_pos[0]) + abs(node_pos[1] - end_pos[1])


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


def astar(obstacle_map, start, end, clearance):
    iterations = 0
    max_iterations = (max(len(obstacle_map), len(obstacle_map[0])) // 2) ** 10


    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0


    open_list = []
    closed_list = []
    open_list.append(start_node)


    while len(open_list) > 0:
        iterations += 1


        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index


        if iterations > max_iterations:
            print("Giving up")
            return get_path(current_node)


        open_list.pop(current_index)
        closed_list.append(current_node)


        if current_node == end_node:
            return get_path(current_node)


        children_pos = get_neighbors_pos(current_node.position, obstacle_map)
        children = []
        for i in range(len(children_pos)):
            children.append(Node(current_node, children_pos[i]))


        for child in children:
            if len([visited_child for visited_child in closed_list if visited_child == child]) > 0:
                continue


            child.g = current_node.g + 1
            child.h = heuristic(child.position, end)
            child.f = child.g + child.h


            if len([i for i in open_list if child == i and child.g > i.g]) > 0:
                continue


            if passes_clearance(child.position, obstacle_map, clearance):
                open_list.append(child)


def get_instructions(path, orientation):
    curr_point = path[0]
    pivot = path[0]


    instructions = []


    for next_point in path[1:]:
        next_x = next_point[0]
        next_y = next_point[1]


        if orientation == "North":
            if next_y == curr_point[1] + 1:
                instructions.append("Right")
                instructions.append("Right")
                orientation = "South"
            if next_x == curr_point[0] + 1:
                instructions.append(abs(next_y - pivot[1]))
                instructions.append("Right")
                orientation = "East"
                pivot = curr_point
            elif next_x == curr_point[0] - 1:
                instructions.append(abs(next_y - pivot[1]))
                instructions.append("Left")
                orientation = "West"
                pivot = curr_point


        elif orientation == "South":
            if next_y == curr_point[1] - 1:
                instructions.append("Right")
                instructions.append("Right")
                orientation = "North"
            if next_x == curr_point[0] - 1:
                instructions.append(abs(next_y - pivot[1]))
                instructions.append("Right")
                orientation = "West"
                pivot = curr_point
            elif next_x == curr_point[0] + 1:
                instructions.append(abs(next_y - pivot[1]))
                instructions.append("Left")
                orientation = "East"
                pivot = curr_point


        elif orientation == "East":
            if next_x == curr_point[0] - 1:
                instructions.append("Right")
                instructions.append("Right")
                orientation = "West"
            if next_y == curr_point[1] - 1:
                instructions.append(abs(next_x - pivot[0]))
                instructions.append("Left")
                orientation = "North"
                pivot = curr_point
            elif next_y == curr_point[1] + 1:
                instructions.append(abs(next_x - pivot[0]))
                instructions.append("Right")
                orientation = "South"
                pivot = curr_point


        if orientation == "West":
            if next_x == curr_point[0] + 1:
                instructions.append("Right")
                instructions.append("Right")
                orientation = "East"
            if next_y == curr_point[1] - 1:
                instructions.append(abs(next_x - pivot[0]))
                instructions.append("Right")
                orientation = "South"
                pivot = curr_point
            elif next_y == curr_point[1] + 1:
                instructions.append(abs(next_x - pivot[0]))
                instructions.append("Left")
                orientation = "North"
                pivot = curr_point


        curr_point = next_point


    if orientation == "North" or orientation == "South":
        instructions.append(abs(curr_point[1] - pivot[1]))


    if orientation == "East" or orientation == "West":
        instructions.append(abs(curr_point[0] - pivot[0]))


    return instructions


def main():
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


    get_instructions(astar(maze, start, end, clearance), orientation)


if __name__ == '__main__':
    main()
