import torch
import numpy as np
from tqdm import tqdm
from typing import Any, List
from lhyra import Optimizer, Lhyra, Solver
import matplotlib.pyplot as plt
from time import time
from random import random

class ValueOptimizer(Optimizer):
    def __init__(self, lhyra: Lhyra):
        """
        Initialize an optimizer.
        :param lhyra: A Lhyra instance to optimize.
        :param gamma: Discount factor (default 0.99)
        """
        
        super().__init__(lhyra)

        self.values = [
            torch.nn.Linear(lhyra.extractor.shape[0], 1)
            for i in range(len(lhyra.solvers))
        ]

        self.opts = [
            torch.optim.Adam(value.parameters(), lr=1e-2)
            for value in self.values
        ]

        self.loss_fn = torch.nn.MSELoss(reduction='sum')
        self.epochs = []
        self.training = False
        self.gen_params()


    def train(self, iters: int=1000, plot=False):
        """
        Train the classifier on the data, given a hook into
        the Lhyra object's eval method.
        
        :param iters: Number of training iterations to run.
        :param plot: Show a plot.
        """
        
        self.training = True

        data = self.lhyra.data_store.get_data(iters)

        totals = []
        self.p = 1
        for episode, datum in enumerate(tqdm(data)):
            self.p = 0.99 * self.p

            self.lhyra.clear()
            self.epochs.clear()
            
            self.lhyra.eval(datum)
            
            totals.append(self.lhyra.times[0])

            for x, y in zip(self.epochs, self.lhyra.times):
                action, features = x

                out = torch.FloatTensor([y])
                inp = torch.FloatTensor(features)

                out_pred = self.values[action](inp)
                loss = self.loss_fn(out_pred, out)

                self.values[action].zero_grad()
                loss.backward()
                self.opts[action].step()

            self.gen_params()

        vals = [
            sum(totals[i:i + iters//100])/(iters//100)
            for i in range(0,iters,iters//100)
        ]

        self.training = False

        plt.plot(vals)
        plt.show()

    def gen_params(self):
        self.params = [
            tuple(
                param.data.item()
                for name, param in value.named_parameters()
                if param.requires_grad
            ) for value in self.values
        ]

    def solver(self, features: List) -> Solver:
        """
        Pick and parametrize a solver from the bag of solvers.
        :param features: Features provided to inform solver choice.
        :return: The Solver best suited given the features provided.
        """
        
        size = len(self.lhyra.solvers)
        
        values = [weight*features[0] + bias for weight, bias in self.params]

        # values = []
        # for state in potential_actions:
        #     values.append(self.params['0.bias'][0] + sum(a*b for a,b in zip(state, self.params['0.weight'][0])))

        if self.training:
            values = torch.FloatTensor(values)

            values -= values.min() - 1

            probs = (1/values) / torch.sum(1/values)

            m = torch.distributions.Categorical(probs)
            action = m.sample().item()

            self.epochs.append((action, features))
        else:
            action = values.index(min(values))
            

        if self.lhyra.vocal:
            print(self.lhyra.solvers[action])

        return self.lhyra.solvers[action].parametrized({})