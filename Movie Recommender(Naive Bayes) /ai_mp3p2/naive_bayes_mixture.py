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
This is the main entry point for Part 2 of this MP. You should only modify code
within this file for Part 2 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


import numpy as numpy
import math
from collections import Counter





def naiveBayesMixture(train_set, train_labels, dev_set, bigram_lambda,unigram_smoothing_parameter, bigram_smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    bigram_lambda - float between 0 and 1

    unigram_smoothing_parameter - Laplace smoothing parameter for unigram model (between 0 and 1)

    bigram_smoothing_parameter - Laplace smoothing parameter for bigram model (between 0 and 1)

    pos_prior - positive prior probability (between 0 and 1)
    """
    
    devl = []
    upt = Counter()
    unt = Counter()
    bpt = Counter()
    bnt = Counter()

    # TODO: Write your code here
    for rev in train_set:
        if(train_labels[train_set.index(rev)]==1):
            for word in rev:
                upt[word]+=1
        else:
            for word in rev:
                unt[word]+=1
   
    uptot = sum(upt.values())
    untot = sum(unt.values())

    for rev in train_set:
        if(train_labels[train_set.index(rev)]==1):
            for i in range(len(rev)-1):
                bword = rev[i] + rev[i+1]
                bpt[bword]+=1
        else:
            for i in range(len(rev)-1):
                bword = rev[i] + rev[i+1]
                bnt[bword]+=1
    bptot = sum(bpt.values())
    bntot = sum(bnt.values())

    for dev in dev_set:
        up = 0
        un = 0
        bp = 0
        bn = 0
        for word in dev:
            up += math.log10((upt[word]+unigram_smoothing_parameter)/(uptot+unigram_smoothing_parameter*2))
            un += math.log10((unt[word]+unigram_smoothing_parameter)/(untot+unigram_smoothing_parameter*2))
        for i in range(len(dev)-1):
            bword = dev[i]+dev[i+1]
            bp += math.log10((bpt[bword]+bigram_smoothing_parameter)/(bptot+bigram_smoothing_parameter*2))
            bn += math.log10((bnt[bword]+bigram_smoothing_parameter)/(bntot+bigram_smoothing_parameter*2))
        pprob = (1-bigram_lambda)*(math.log10(pos_prior)+up) + (bigram_lambda)*(math.log10(pos_prior)+bp)
        nprob = (1-bigram_lambda)*(math.log10(1-pos_prior)+un) + (bigram_lambda)*(math.log10(1-pos_prior)+bn)

        if(nprob < pprob):
            devl.append(1)
        else:
            devl.append(0)
    # return predicted labels of development set (make sure it's a list, not a numpy array or similar)
    return devl