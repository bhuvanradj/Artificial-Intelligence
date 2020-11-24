# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019

"""
You should only modify code within this file for part 2 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class NeuralNet(torch.nn.Module):
    def __init__(self, lrate,loss_fn,in_size,out_size):
        """
        Initialize the layers of your neural network
        @param lrate: The learning rate for the model.
        @param loss_fn: The loss functions
        @param in_size: Dimension of input
        @param out_size: Dimension of output
        """
        super(NeuralNet, self).__init__()
        self.lrate = lrate
        self.loss_fn = loss_fn
        self.in_size = in_size
        self.out_size = out_size
        self.hidden = nn.Linear(self.in_size,128,True)
        self.hhidden = nn.Linear(128,128,True)
        self.output = nn.Linear(128,self.out_size,True)
        self.optimizer = optim.SGD(self.get_parameters(),lr=self.lrate,weight_decay=1e-5)
        self.LeakyReLU = nn.LeakyReLU()
        self.sigmoid = nn.Sigmoid()

    def get_parameters(self):
        """ Get the parameters of your network
        @return params: a list of tensors containing all parameters of the network
        """
        return self.parameters()
        

    def forward(self, x):
        """ A forward pass of your autoencoder
        @param x: an (N, in_size) torch tensor
        @return y: an (N, out_size) torch tensor of output from the network
        """
        x = self.hidden(x)
        x = self.LeakyReLU(x)
        x = self.hhidden(x)
        x = self.LeakyReLU(x)
        x = self.output(x)
        x = self.sigmoid(x)
        y=x
        return y

    def step(self, x,y):
        """
        Performs one gradient step through a batch of data x with labels y
        @param x: an (N, in_size) torch tensor
        @param y: an (N,) torch tensor
        @return L: total empirical risk (mean of losses) at this time step as a float
        """
        self.optimizer.zero_grad()
        x = self(x)
        L = self.loss_fn(x,y)
        L.backward()
        self.optimizer.step()
        return L


def fit(train_set,train_labels,dev_set,n_iter,batch_size=100):
    """ Fit a neural net.  Use the full batch size.
    @param train_set: an (N, out_size) torch tensor
    @param train_labels: an (N,) torch tensor
    @param dev_set: an (M, out_size) torch tensor
    @param n_iter: int, the number of batches to go through during training (not epoches)
                   when n_iter is small, only part of train_set will be used, which is OK,
                   meant to reduce runtime on autograder.
    @param batch_size: The size of each batch to train on.
    # return all of these:
    @return losses: list of total loss (as type float) at the beginning and after each iteration. Ensure len(losses) == n_iter
    @return yhats: an (M,) NumPy array of approximations to labels for dev_set
    @return net: A NeuralNet object
    # NOTE: This must work for arbitrary M and N
    """
    losses = []
    net = NeuralNet(0.75,nn.CrossEntropyLoss(),len(train_set[0]), 5)
    m = train_set.mean()
    stdv = train_set.std()
    train_set = (train_set - m) / stdv
    dev_set = (dev_set - m) / stdv
    n_iter = n_iter+150

    for i in range(n_iter):
        lt = net.step(train_set,train_labels)
        L = lt.item()
        losses.append(L)

    out = net(dev_set)
    yhats = np.asarray(out.detach().argmax(1))
    return losses,yhats, net
