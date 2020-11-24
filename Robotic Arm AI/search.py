# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,astar)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze

from collections import deque
from heapq import heappop, heappush
import queue

def search(maze, searchMethod):
    return {
        "bfs": bfs,
    }.get(searchMethod, [])(maze)

def bfs(maze):
    # Write your code here
    """
    This function returns optimal path in a list, which contains start and objective.
    If no path found, return None. 
    """
    start = maze.getStart()
    dots = maze.getObjectives()
    goal = dots[0]
    Q = queue.deque()
    vis = []
    p = []
    paths = {}
    
    Q.append(start)
    vis.append(start)
    paths[start] = None
    p.append(goal)

    while (Q):
        cur = Q.popleft()
        ngb = maze.getNeighbors(cur[0],cur[1])
        
        for n in ngb:
            if (n not in vis and maze.isValidMove(n[0],n[1])==True):
                Q.append(n)
                vis.append(n)
                paths[n] = cur
    
    itr = goal
    while(itr!=start):
        p.append(paths[itr])
        itr = paths[itr]
    p.append(start)
    p.reverse()
    p.pop(0)
    if(goal in p):
        return p
    else: return None
    
