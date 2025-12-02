import numpy as np
import random
import time
import math
import sys
import os
time = 55.0  

def readData(file):
    with open(file, 'r') as f:
        lines = f.readlines()

    nodes = int(lines[0].strip())

    distances = np.zeros((nodes, nodes))
    for stuff in entry[2:]:
        parts = stuff.split()
        distance = float(parts[2])
        distances[int(parts[0]) - 1, int(parts[1]) - 1] = distance
        distances[int(parts[0]) - 1, int(parts[1]) - 1] = distance
    
    return nodes, distances
def writeSol(path):
    i = 0
    length = len(path)
    with open("920784024_solution.txt", 'w') as file:
        for node in path:
            if i<length-1:
                file.write(f"{node + 1}, ")
            else:
                file.write(f"{node + 1}")
                file.write("\n")
            i = i+1

