import numpy as np
import matplotlib.pyplot as plt
import random
import settings

def build_maze():
    maze = []
    graph_size = 100
    for i in range(graph_size):
        tmp = []
        for j in range(graph_size):
            if ((j == int(.25 * graph_size) or j == int(.25 * graph_size)+1) or (j == int(.75 * graph_size) or j == int(.75 * graph_size)+1)) and i > int(.6 * graph_size):
                tmp.append(1)
            elif (j == int(.50 * graph_size) or j == int(.50 * graph_size)+1) and i < int(.4 * graph_size):
                tmp.append(1)
            else:
                x = random.randint(-1,0)
                tmp.append(x)
        maze.append(tmp)
    return maze

def pretty_printing(graph):
    settings.im_count +=1
    plt.imshow(graph,interpolation='none')
    plt.savefig('current_map.png')
    

pretty_printing(build_maze())
pretty_printing(build_maze())