
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.
    
        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """

    mmap=[[]]
    angles = arm.getArmAngle()
    maxa = arm.getArmLimit()
    alpha = maxa[0][0]
    beta = maxa[1][0]
    rows = int((maxa[0][1]-alpha)/granularity+1) 
    cols = int((maxa[1][1]-beta)/granularity+1)
    mmap = [[SPACE_CHAR for c in range(0,cols)] for r in range(0,rows)]
    offsets = (maxa[0][0],maxa[1][0])
    start = angleToIdx(angles,offsets,granularity)

    for r in range(rows):
        for c in range(cols):
            a = idxToAngle((r,c),offsets,granularity)
            arm.setArmAngle(a)
            if(not isArmWithinWindow(arm.getArmPos(),window)):
                mmap[r][c]= WALL_CHAR
            elif(doesArmTouchObjects(arm.getArmPosDist(),obstacles,isGoal=False)):
                mmap[r][c] = WALL_CHAR          
            elif(doesArmTipTouchGoals(arm.getArmPosDist()[1][1],goals)):
                mmap[r][c] = OBJECTIVE_CHAR
            elif (doesArmTouchObjects(arm.getArmPosDist(), goals, isGoal=True)):
                mmap[r][c] = WALL_CHAR

    mmap[start[0]][start[1]] = START_CHAR
    return Maze(mmap,[maxa[0][0],maxa[1][0]],granularity)

   