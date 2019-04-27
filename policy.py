import torch
import numpy as np
from tqdm import tqdm
from typing import Any, List
from lhyra import Optimizer, Lhyra, Solver

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

        self.opt = torch.optim.Adam(self.policy.parameters())
        self.eps = np.finfo(np.float32).eps.item()
        self.saved_log_probs = []

    def train(self, iters: int=1000):
        """
        Train the classifier on the data, given a hook into
        the Lhyra object's eval method.
        
        :param iters: Number of training iterations to run.
        """

        data = self.lhyra.data_store.get_data(iters)

        for episode, datum in enumerate(tqdm(data)):
            self.lhyra.clear()
            self.lhyra.eval(datum)
            
            rewards = [1/t for t in self.lhyra.times]
            returns = []
            policy_loss = []
            R = 0

            for r in rewards:
                R = r + self.gamma * R
                returns.insert(0,R)

            returns = torch.tensor(returns)
            rns = (returns - returns.mean()) / (returns.std() + self.eps)

            for log_prob, R in zip(self.saved_log_probs, returns):
                policy_loss.append(-log_prob * R)

            self.opt.zero_grad()
            policy_loss = torch.cat(policy_loss).sum()
            policy_loss.backward()

            self.opt.step()
            self.saved_log_probs.clear()


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

        return self.lhyra.solvers[action.item()].parametrized({})