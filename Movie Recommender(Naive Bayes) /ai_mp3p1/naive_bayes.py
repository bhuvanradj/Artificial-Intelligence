# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018
# Modified by Jaewook Yeom 02/02/2020

"""
This is the main entry point for Part 1 of MP3. You should only modify code
within this file for Part 1 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as numpy
import math
from collections import Counter


def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter you provided with --laplace (1.0 by default)

    pos_prior - positive prior probability (between 0 and 1)
    """
    devl = []
    pt = Counter()
    nt = Counter()
    

    # TODO: Write your code here
    for rev in train_set:
        if(train_labels[train_set.index(rev)]==1):
            for word in rev:
                pt[word]+=1
        else:
            for word in rev:
                nt[word]+=1
   
    ptot = sum(pt.values())
    ntot = sum(nt.values())
    
    for dev in dev_set:
        pp=0
        np=0
        for word in dev:
            pp+=math.log10((pt[word]+smoothing_parameter)/(ptot+smoothing_parameter*2))
            np+=math.log10((nt[word]+smoothing_parameter)/(ntot+smoothing_parameter*2))
        pprob = math.log10(pos_prior) + pp
        nprob = math.log10(1-pos_prior) + np
        if(nprob < pprob):
            devl.append(1)
        else:
            devl.append(0)
    # return predicted labels of development set (make sure it's a list, not a numpy array or similar)
    return devl