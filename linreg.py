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
        self.regr.fit([0 for n in range(len(lhyra.extractor.shape[0]))], [0]) # Initialize with 0s

        self.eps_bounds = eps_bounds

        self.epochs = []
        self.training = False


    def train(self, iters: int=100, iterdata: int=40, plot=False):
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

        for episode in enumerate(tqdm(iter)):

        	totaltimes.append(0)

        	# epsilon for eps-greedy policy
        	self.eps = self.eps_bounds[0] + (episode/(iter-1))*(self.eps_bounds[1]-self.eps_bounds[0])

        	data = self.lhyra.data_store.get_data(iterdata)
        	for datum in data:

	            self.lhyra.eval(datum)

	            totaltimes[-1] += self.lhyra.times[0]
	            for (a, f), t in zip(self.epochs, self.lhyra.times):
	            	feature_set[a].append(f)
	            	times[a].append(t)

		        self.epochs.clear()
	            self.lhyra.clear()

	        for a, r in enumerate(self.regr):
            	r.train(features[a], times[a])

           	totaltimes[-1] /= iterdata

        self.training = False

        plt.plot(list(range(1,iter+1)), totaltimes)
        plt.show()

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

        if self.training and random() < self.eps:
    		action = randint(0,len(self.lhyra.solvers)-1)

    	else:
	    	values = [r.predict(features) for r in self.regr]
	    	action = np.argmin(values)

    	if self.training:
            self.epochs.append((action, features))

        if self.lhyra.vocal:
            print(self.lhyra.solvers[action])

        return self.lhyra.solvers[action].parametrized({})