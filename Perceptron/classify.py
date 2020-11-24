# classify.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/27/2018
# Extended by Daniel Gonzales (dsgonza2@illinois.edu) on 3/11/2020

"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.

train_set - A Numpy array of 32x32x3 images of shape [7500, 3072].
            This can be thought of as a list of 7500 vectors that are each
            3072 dimensional.  We have 3072 dimensions because there are
            each image is 32x32 and we have 3 color channels.
            So 32*32*3 = 3072. RGB values have been scaled to range 0-1.

train_labels - List of labels corresponding with images in train_set
example: Suppose I had two images [X1,X2] where X1 and X2 are 3072 dimensional vectors
         and X1 is a picture of a dog and X2 is a picture of an airplane.
         Then train_labels := [1,0] because X1 contains a picture of an animal
         and X2 contains no animals in the picture.

dev_set - A Numpy array of 32x32x3 images of shape [2500, 3072].
          It is the same format as train_set
"""
import math
import numpy as np

def convert(x):
    if x==True:
        return 1
    else:
        return -1

def trainPerceptron(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    # return the trained weight and bias parameters 
    l = len(train_set[0])
    lt = len(train_set)
    W = np.zeros(l)
    b = 0

    for i in range(max_iter):
        for j in range(lt):
            t = train_set[j]
            dot = np.dot(t,W)
            p = np.sign(dot+b)
            if(p<0):
                p=0
            if(p!=train_labels[j]):
                W += learning_rate*(train_labels[j]-p)*t
                b += learning_rate*(train_labels[j]-p)
    return W, b

def classifyPerceptron(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    # Train perceptron model and return predicted labels of development set
    pred = []
    l = len(dev_set)
    W,b = trainPerceptron(train_set,train_labels,learning_rate,max_iter)
    for i in range(l):
        d = dev_set[i]
        dot = np.dot(d,W)
        p = np.sign(dot+b) 
        if(p<0):
            pred.append(0)
        else:
            pred.append(1)
    return pred

def sigmoid(x):
    # TODO: Write your code here
    # return output of sigmoid function given input x 
    return 1 / (1 + math.exp(-x))

def trainLR(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    # return the trained weight and bias parameters 
    l = len(train_set[0])
    lt = len(train_set)
    W = np.zeros(l)
    b = 0

    for i in range(max_iter):
        for j in range(lt):
            t = train_set[j]
            dot = np.dot(t,W)
            tmp = np.sign(dot+b)
            p=sigmoid(tmp)
            if(p<0):
                p=0
            if(p!=train_labels[j]):
                W += learning_rate*(train_labels[j]-p)*t
                b += learning_rate*(train_labels[j]-p)
    return W, b


def classifyLR(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    # Train LR model and return predicted labels of development set
    pred = []
    l = len(dev_set)
    W,b = trainLR(train_set,train_labels,learning_rate,max_iter)
    for i in range(l):
        d = dev_set[i]
        dot = np.dot(d,W)
        tmp = np.sign(dot+b)
        p=sigmoid(tmp) 
        if(p<0):
            pred.append(0)
        else:
            pred.append(1)
    return pred

def classifyEC(train_set, train_labels, dev_set, k):
    # Write your code here if you would like to attempt the extra credit
    return []
