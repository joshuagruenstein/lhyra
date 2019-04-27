import torch
import numpy as np
from tqdm import tqdm
from typing import Any, List
from lhyra import Optimizer, Lhyra, Solver
import matplotlib.pyplot as plt

class ValueOptimizer(Optimizer):
    def __init__(self, lhyra: Lhyra):
        """
        Initialize an optimizer.
        :param lhyra: A Lhyra instance to optimize.
        :param gamma: Discount factor (default 0.99)
        """
        
        super().__init__(lhyra)

        self.value = torch.nn.Sequential(
            torch.nn.Linear(len(self.lhyra.solvers)+lhyra.extractor.shape[0], 1)
        )

        self.opt = torch.optim.Adam(self.value.parameters(), lr=1e-2)
        self.loss_fn = torch.nn.MSELoss(reduction='sum')
        self.epochs = []
        self.training = False


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
        errors = []
        for episode, datum in enumerate(tqdm(data)):
            self.lhyra.clear()
            self.epochs.clear()
            
            self.lhyra.eval(datum)
            totals.append(self.lhyra.times[0])

            x = torch.stack(self.epochs)
            y = torch.FloatTensor(self.lhyra.times)

            y_pred = self.value(x)
            loss = self.loss_fn(y_pred, y)
            errors.append(loss)

            self.value.zero_grad()
            loss.backward()
            self.opt.step()

        vals = [
            sum(totals[i:i + iters//100])/(iters//100)
            for i in range(0,iters,iters//100)
        ]

        errors = [
            sum(errors[i:i + iters//100])/(iters//100)
            for i in range(0,iters,iters//100)
        ]

        plt.plot(errors)

        plt.show()

        self.training = False


    def solver(self, features: List) -> Solver:
        """
        Pick and parametrize a solver from the bag of solvers.
        :param features: Features provided to inform solver choice.
        :return: The Solver best suited given the features provided.
        """

        size = len(self.lhyra.solvers)
        potential_actions = torch.FloatTensor([
            [1 if j==i else 0 for j in range(size)] + features
            for i in range(size)
        ])

        values = self.value(potential_actions).squeeze()

        if self.training:
            probs = torch.nn.functional.softmax(-values,dim=0)

            m = torch.distributions.Categorical(probs)
            action = m.sample().item()

            self.epochs.append(torch.cat((
                potential_actions[action][:-1],
                torch.tensor(features)
            )))
        else:
            val, index = values.min(0, keepdim=True)
            action = index.item() 

        if self.lhyra.vocal:
            print(self.lhyra.solvers[action])

        return self.lhyra.solvers[action].parametrized({})