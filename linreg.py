from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

import numpy as np
from tqdm import tqdm
from typing import Any, List
from lhyra import Optimizer, Lhyra, Solver
import matplotlib.pyplot as plt
from time import time
from random import random, randint

class LinOptimizer(Optimizer):
    def __init__(self, lhyra: Lhyra, eps_bounds=(0.9,0.1)):
        """
        Initialize an optimizer.
        :param lhyra: A Lhyra instance to optimize.
        :param gamma: Discount factor (default 0.99)
        """
        
        super().__init__(lhyra)

        self.regr = [linear_model.LinearRegression() for s in self.lhyra.solvers] # Could change models
        for r in self.regr:
            r.fit([[0 for n in range(lhyra.extractor.shape[0])]], [0]) # Initialize with 0s

        self.eps_bounds = eps_bounds

        self.epochs = []
        self.training = False


    def train(self, iters: int=100, sample: int=40, plot=False):
        """
        Train the classifier on the data, given a hook into
        the Lhyra object's eval method.
        
        :param iters: Number of training iterations to run.
        :param plot: Show a plot.
        """
        
        self.training = True

        features = [[] for s in self.lhyra.solvers]
        times = [[] for s in self.lhyra.solvers]

        totaltimes = []

        for episode in tqdm(range(iters)):

            totaltimes.append(0)

            # epsilon for eps-greedy policy
            self.eps = self.eps_bounds[0] + (episode/(iters-1))*(self.eps_bounds[1]-self.eps_bounds[0])

            data = self.lhyra.data_store.get_data(sample)
            for datum in data:

                self.lhyra.eval(datum)

                totaltimes[-1] += self.lhyra.times[0]
                for (a, f), t in zip(self.epochs, self.lhyra.times):
                    features[a].append(f)
                    times[a].append(t)

                self.epochs.clear()
                self.lhyra.clear()

            for a, r in enumerate(self.regr):
                if len(features[a]) > 0:
                    r.fit(features[a], times[a])

            totaltimes[-1] /= sample

        self.training = False

        plt.plot(list(range(1,iters+1)), totaltimes)
        plt.show()

    def solver(self, features: List) -> Solver:
        """
        Pick and parametrize a solver from the bag of solvers.
        :param features: Features provided to inform solver choice.
        :return: The Solver best suited given the features provided.
        """
        
        size = len(self.lhyra.solvers)

        if self.training and random() < self.eps:
            action = randint(0,size-1)

        else:
            values = [r.predict([features]) for r in self.regr]
            action = np.argmin(values)

        if self.training:
            self.epochs.append((action, features))

        if self.lhyra.vocal:
            print(self.lhyra.solvers[action])

        return self.lhyra.solvers[action].parametrized({})