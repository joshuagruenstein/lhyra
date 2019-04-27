import torch
import numpy as np
from tqdm import tqdm
from typing import Any, List
from lhyra import Optimizer, Lhyra, Solver
import matplotlib.pyplot as plt
from random import random
from functools import reduce
from copy import deepcopy
from math import exp

class PolicyLinearOptimizer(Optimizer):
    def __init__(self, lhyra: Lhyra, gamma: float=0.99):
        """
        Initialize an optimizer.
        :param lhyra: A Lhyra instance to optimize.
        :param gamma: Discount factor (default 0.99)
        """
        
        super().__init__(lhyra)

        self.gamma = gamma

        self.policy = torch.nn.Sequential(
            torch.nn.Linear(lhyra.extractor.shape[0], len(lhyra.solvers)),
            torch.nn.Softmax(dim=0)
        )

        for name, param in self.policy.named_parameters():
            if param.requires_grad:
                print(name, param.data)


        self.opt = torch.optim.Adam(self.policy.parameters())
        self.eps = np.finfo(np.float32).eps.item()
        self.saved_log_probs = []

    def train(self, iters: int=1000, plot=False):
        """
        Train the classifier on the data, given a hook into
        the Lhyra object's eval method.
        
        :param iters: Number of training iterations to run.
        :param plot: Show a plot.
        """

        data = self.lhyra.data_store.get_data(iters)

        totals = []
        for episode, datum in enumerate(tqdm(data)):
            self.lhyra.clear()
            self.lhyra.eval(datum)
            totals.append(self.lhyra.times[0])

            rewards = [-t for t in self.lhyra.times]
            returns = []
            policy_loss = []
            R = 0

            for r in rewards:
                R = r + self.gamma * R
                returns.insert(0,R)

            returns = torch.tensor(returns)
            rns = (returns - returns.mean()) / (returns.std() + self.eps)

            for log_prob, R in zip(self.saved_log_probs, returns):
                policy_loss.append(log_prob * R)

            self.opt.zero_grad()
            policy_loss = torch.cat(policy_loss).sum()
            policy_loss.backward()

            self.opt.step()
            self.saved_log_probs.clear()
        
        vals = [
            sum(totals[i:i + iters//100])/100
            for i in range(0,iters,iters//100)
        ]

        plt.plot(vals)

        plt.show()


    def solver(self, features: List) -> Solver:
        """
        Pick and parametrize a solver from the bag of solvers.
        :param features: Features provided to inform solver choice.
        :return: The Solver best suited given the features provided.
        """

        state = torch.FloatTensor(features).unsqueeze(0)
        probs = self.policy(state)

        m = torch.distributions.Categorical(probs)
        action = m.sample()

        self.saved_log_probs.append(m.log_prob(action))

        if self.lhyra.vocal:
            print(self.lhyra.solvers[action.item()])

        return self.lhyra.solvers[action.item()].parametrized({})
        
def SAOptimizer(Optimizer):
    def __init__(self, lhyra: Lhyra, agg: float=0.5):
        """
        Initialize an optimizer.
        :param lhyra: A Lhyra instance to optimize.
        :param gamma: Discount factor (default 0.99)
        """
        
        super().__init__(lhyra)
        
        self.lhyra = lyra
        
        self.policy = [[random() for t in 2**len(lhyra.extractor.shape[0])] for s in lhyra.solvers]: # Assuming 1D feature vect

        self.agg = agg # Aggressiveness of training parameters

        
        
    def train(self, iters: int=1000, sample=100, plot=False):
        """
        Train the classifier on the data, given a hook into
        the Lhyra object's eval method.
        
        :param iters: Number of training iterations to run.
        :param plot: Show a plot.
        """
        
    
        data = self.lhyra.data_store.get_data(sample)
        
        self.prev_time = 999999999
        
        times = []
        
        for i in range(iters):
            temperature = min(exp(-4*i/iters), .5)
        
            time = 0
            for episode, datum in enumerate(tqdm(data)):
                self.lhyra.clear()
                self.lhyra.eval(datum)
                time += self.lhyra.times[0] # Get the total time
            times.append(time)
                
            if time < self.prev_time or random() < temperature:
                self.prev_policy = deepcopy(self.policy)
                self.prev_time = time
                
            # Perturb. Decrease perturb sizes over time.
            self.policy = [[t+(self.agg*random()-self.agg)*(1-i/iters) for t in s] for s in self.prev_policy]
        
        self.policy = self.prev_policy # Don't use the last one, use the second-to-last

        plt.plot(range(iters), times)

        plt.show()
        
        
    def solver(self, features: List) -> Solver:
        """
        Pick and parametrize a solver from the bag of solvers.
        :param features: Features provided to inform solver choice.
        :return: The Solver best suited given the features provided.
        """

        ans = max(self.policy, self.key=lambda s: sum([reduce([features[n] for n in range(len(features)) if i&(2**n)],
                            lambda x, y: x*y) for i, t in enumerate(s)]))
        
        if self.lhyra.vocal:
            print(ans)

        return ans