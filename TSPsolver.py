import numpy as np
import random
import time
import math
import sys
import os
limit = 55.0  

def readData(file):
    #data parsing using 0 index unlike the actual graphs
    with open(file, 'r') as f:
        entry = f.readlines()

    nodes = int(entry[0].strip())

    distances = np.zeros((nodes, nodes))
    for stuff in entry[2:]:
        parts = stuff.split()
        distance = float(parts[2])
        distances[int(parts[0]) - 1, int(parts[1]) - 1] = distance
        distances[int(parts[0]) - 1, int(parts[1]) - 1] = distance
    
    return nodes, distances
def writeSol(path):
    #just writes the solutions as specified in the hw
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

def nearestNeighbor(distance, nodes):
    #literally just a generic algorithm for a typical cycle
    start = nodes-1
    toVisit = set(range(nodes-1))
    
    path = [start]

    while len(toVisit)>0:
        next = min(toVisit, key = lambda node: distance[start, node])
        toVisit.remove(next)
        path.append(next)
        start = next
    return path

def calcPathCost(distances, path, nodes):
    #literally just sums the distances
    length = 0
    for i in range(nodes):
        length = length + distances(path[i],path[i+1])
    return length

def reverse(path,start, end):
    #literally just an array reversal helper for 2 opt 
    while start<end:
        x = path[start]
        path[start] = path[end]
        path[end] = x
        left = left + 1
        right = right+1

def two_opt(currPath, distances, start, max_time):
    best = list(currPath)
    currBestCost = calcPathCost(distances, currPath, len(currPath))
    checkOpt = True

    while checkOpt == True:
        checkOpt = False
        if time.time()-start > limit:
            break
        #check possible swap for a better path
        for i in range(1,len(currPath)-1):
            if time.time()-start > limit:
                break
            #iterate for ith and remaining parts of the cycle and keep shifting for optimality
            for j in range(i+1, len()):
                bufPrev = best[i-1]
                bufCur = best[i+1]

                checkChange = best[j]
                checkAfterChange = best[(j+1)%len(currPath)]

                #two op distance
                diff = distances[bufPrev, checkChange]+ distances[bufCur,checkAfterChange]-distances[bufPrev,bufCur]-distances[checkChange,checkAfterChange]
                if diff<0:
                    #we found a better path, need to change the order by algorithm
                    reverse(best, i, j)
                    currBestCost = currBestCost + diff
                    checkOpt = True
                    break
                if checkOpt:
                    break
    return best, currBestCost

def solve(distances, nodes):
    start = time.time()

    #heuristic, get a random path using nearest neighbor stuff
    currPath = nearestNeighbor(distances, nodes)
    currLen = calcPathCost(distances, nodes)

    iterPath = currPath
    iterLen = currLen
    #temp annealing stuff, start at 250, end at something small
    tempStart = 250
    tempEnd = 0.01
    #allocate some time specifically for annealing ONLY, 50 seconds
    annealTime = 50.0

    numIters = 0
    while True:
        numIters = numIters +1

        if time.time()-start >=annealTime:
            break

        newTemp = tempStart * pow((tempEnd/tempStart),(time.time()-start)/annealTime)
        #do the two opt, select two random numbers, ST i<j
        i = random.randint(1,nodes-1)
        j = random.randint(1,nodes-1)
        i, j = min(i,j), max(i,j)
        #exact same as prev 2 op fxn
        bufPrev = iterPath[i-1]
        bufCur = iterPath[i+1]
        checkChange = iterPath[j]
        checkAfterChange = iterPath[(j+1)%len(iterPath)]

        #two op distance
        diff = distances[bufPrev, checkChange]+ distances[bufCur,checkAfterChange]-distances[bufPrev,bufCur]-distances[checkChange,checkAfterChange]
        #accept better path if we find it
        if diff<0:
            reverse(iterPath, i, j)
            iterLen = iterLen + diff
            #iter path will randomly take worse paths so we need to keep checking this
            if iterLen<currLen:
                currLen = iterLen
                currPath = iterPath

        else:
            #randomly accept a path of increasing cost (the point of annealing)
            if random.random()<math.exp(-diff/(newTemp)):
                reverse(iterPath,i,j)
                iterLen = iterLen+diff
    tot = time.time()-start
    print("Best cost found: {currLen}\n")
    print("Amount of Cycles: {numIters}")
    print("Time Taken: {tot}")
    writeSol(currPath)


print("Starting Euclidean\n")
nodes, distances = readData("TSP_1000_euclideanDistance.txt")
solve(distances, nodes)
print("Starting Random")
nodes, distances = readData("TSP_1000_randomDistance.txt")
solve(distances, nodes)


