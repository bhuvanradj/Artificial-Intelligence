# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,extra)
from itertools import groupby
import math
import queue

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "extra": extra,
    }.get(searchMethod)(maze)


def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    start = maze.getStart()
    dots = maze.getObjectives()
    goal = dots[0]
    Q = queue.Queue()
    vis = []
    p = []
    paths = {}
    
    Q.put(start)
    vis.append(start)
    paths[start] = None
    p.append(goal)

    while (not Q.empty()):
        cur = Q.get()
        ngb = maze.getNeighbors(cur[0],cur[1])
        
        for n in ngb:
            if (n not in vis and maze.isValidMove(n[0],n[1])):
                Q.put(n)
                vis.append(n)
                paths[n] = cur
    
    itr = goal
    while(itr!=start):
        p.append(paths[itr])
        itr = paths[itr]
    p.append(start)
    p.reverse()
    p.pop(0)
                     
    return p


def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    start = maze.getStart()
    dots = maze.getObjectives()
    goal = dots[0]
    openl = []
    closel = []
    path = {}
    f = {}
    g = {}
    h = {}

    g[start] = 0
    h[start] = manh_dist(start,goal)
    f[start] = g[start] + h[start]
    openl.append(start)
    
    while(len(openl)!=0):
        q = minf(openl,g,h)
        closel.append(q)
        openl.remove(q)

        if(q==goal):
            tmp = []
            itr = goal
            tmp.append(itr)
            while(itr!=start):
                tmp.append(path[itr])
                itr = path[itr]
            tmp.append(start)
            tmp.reverse()
            tmp.pop(0)
            
            return tmp

        ngb = maze.getNeighbors(q[0],q[1])         
        for n in ngb:
            if(not maze.isValidMove(n[0],n[1]) or n in closel):
                continue
            else:
                if(n not in openl):
                    openl.append(n)
                    path[n] = q
                    g[n] = g[q] + 1
                    h[n] = manh_dist(n,goal)
                    f[n] = g[n] + h[n]
                elif(n in openl):
                    if(g[n]>g[q]+1):
                        path[n] = q
                        g[n] = g[q] + 1
                        h[n] = manh_dist(n,goal)
                        f[n] = g[n] + h[n]


def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.
        
    @param maze: The maze to execute the search on.
        
    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here

    return astar_multi(maze)

def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    
    mst = minspantree(maze)
    #print(mst)
    start = mst.pop(0)
    path = []
    '''
    mstdic = {}
    order={}
    for m in mst:
        mstdic[m] = len(multhelp(maze,m,start))-2
    mstdic = sorted(mstdic.items(),key=lambda x: x[1])
    
    f1 = mstdic[-1][0]
    f2 = mstdic[-2][0]
    
    while(len(mstdic)>2):
        x=len(multhelp(maze,f1,f2))-2
        y=len(multhelp(maze,f2,start))-2
        order[f2]=x+y
        mstdic.remove(mstdic[-2])
        f1 = mstdic[-1][0]
        f2 = mstdic[-2][0]
    dict(mstdic)
   # print(order)
    '''

    while(len(mst)!=0):
        v = mst[0]
        mst.remove(v)
        p = multhelp(maze,v,start)
        path.extend(p)
        start = p[-1]
    '''
    i=0
    while(i<len(path)-1):
        if(path[i]==path[i+1]):
            path.remove(path[i+1])
        i=i+1
    i=0
    while(i<len(path)-1):
        if(path[i]==path[i+1]):
            path.remove(path[i+1])
        i=i+1
    '''
    actpath = [i[0] for i in groupby(path)]
    #print('----------',actpath)
    return actpath
    


def multhelp(maze,start,goal):
    """
    Same function as astar, but modified slightly for parts 2 and 3
    Returns astar path from start to goal inputs in given maze

    @param maze: Input maze

    @param: start: start position

    @param goal: goal position
    """
    openl = []
    closel = []
    path = {}
    f = {}
    g = {}
    h = {}

    g[start] = 0
    h[start] = manh_dist(start,goal)
    f[start] = g[start] + h[start]
    openl.append(start)
    
    while(len(openl)!=0):
        q = minf(openl,g,h)
        closel.append(q)
        openl.remove(q)

        if(q==goal):
            tmp = []
            itr = goal
            tmp.append(itr)
            while(itr!=start):
                tmp.append(path[itr])
                itr = path[itr]
            tmp.append(start)
            tmp.pop(-1)
            return tmp

        ngb = maze.getNeighbors(q[0],q[1])         
        for n in ngb:
            if(not maze.isValidMove(n[0],n[1]) or n in closel):
                continue
            else:
                if(n not in openl):
                    openl.append(n)
                    path[n] = q
                    g[n] = g[q] + 1
                    h[n] = manh_dist(n,goal)
                    f[n] = g[n] + h[n]
                elif(n in openl):
                    if(g[n]>g[q]+1):
                        path[n] = q
                        g[n] = g[q] + 1
                        h[n] = manh_dist(n,goal)
                        f[n] = g[n] + h[n]

   

def manh_dist(cur,goal):
    """
    Returns Manhattan Distance from current position to goal position.

    @param cur: current position in maze.

    @param goal: goal destination

    @return dist: Manhattan Distance from cur to goal
    
    """
    
    h = abs(cur[0]-goal[0]) + abs(cur[1]-goal[1])
    return h

def minf(openl,g,h):
    """
    Returns the position with the minimum f=g+h value on the openl list

    @param openl: Open list of positions

    @param g: Dictionary for position and distance from start pairings

    @param h: Dictionary for position and distance to goal pairings
    
    @return minpos: Position with the least f=g+h score
    """
    
    tmp = {}
    for k in openl:
        tmp[k] = g[k]+h[k]
    minpos = min(tmp,key=tmp.get)
    return minpos

def minspantree(maze):
    """
    Returns the MST in set of ordered coordinates

    @param maze: Input maze

    @return mstset: Minimum Spanning set of coordinates
    """
    start = maze.getStart()
    dots = maze.getObjectives()
    mst = {}
    mstset = []
    for d in dots:
            mst[d] = math.inf
    mst[start] = 0
    num=len(mst)

    while(len(mstset)!= num):
        cur = min(mst,key=mst.get)
        del mst[cur]
        if(cur not in mstset):
            mstset.append(cur)
            for v in dots:
                if(v!=cur and v in mst):
                    if(mst[v] > manh_dist(cur,v)):
                        mst[v] = manh_dist(cur,v)
                        #print(mst)
                        #print(mstset)
    return mstset

def extra(maze):
    """
    Runs extra credit suggestion.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return astar_multi(maze)
