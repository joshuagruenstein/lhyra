from random import random, shuffle, randint
import math
from time import time, sleep
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
from lhyra import Solver, FeatureExtractor

def random_points(length: int=100):
    
    return [(random(), random()) for _ in range(length)]

class PointsFeatureExtractor(FeatureExtractor):
    @property
    def shape(self):
        """
        Get the output shape of the feature extractor.
        :return: A list of integers representing the output's dimensions.
        """
        return [1] # Length, (mean, variance)?

    def __call__(self, data):
        """
        Call extractor on given data.
        :param data: A piece of data to extract the parameters of.
        :return: Floats between 0 and 1 of shape self.shape.
        """

        return [len(data)]

def point_dist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def points_brute(points, hook, _={}):
    min_dist = float('inf')
    closest_pair = None
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            p, q = points[i], points[j]
            if point_dist(p,q) < min_dist:
                min_dist = point_dist(p,q)
                closest_pair = (p,q)

    return closest_pair,0

def points_smart(points, hook, _={}):
    #sleep(0.00001)
    if len(points) <= 3:  
        return points_brute(points,None) 

    psorted = sorted(points, key=lambda p:p[0])
    right, right_overhead = hook(psorted[:len(psorted)//2])
    left, left_overhead = hook(psorted[len(psorted)//2:])

    mid = psorted[len(psorted)//2][0]

    dleft, dright = point_dist(*left), point_dist(*right)
    d = min(dleft, dright)

    strip = []
    for x,y in points:
        if point_dist((x,y),(mid,y)) <= d:
            strip.append((x,y))

    strip = sorted(strip, key=lambda p:p[1])

    min_dist = d
    closest_pair = None
    for i, point in enumerate(strip):
        for j in range(i+1, min(len(strip),i+8)):
            if point_dist(point,strip[j]) < min_dist:
                min_dist = point_dist(point,strip[j])
                closest_pair = (point,strip[j])

    if closest_pair is None:
        return (left if dleft < dright else right), right_overhead + left_overhead

    return closest_pair, right_overhead + left_overhead


# def timer(func, iters=10):
#     start = time()
#     for _ in range(iters):
#         func()
#     return (time() - start)/iters

# dataset = [[(random(), random()) for _ in range(2**i)] for i in range(1,10)]

# dumb = [timer(lambda:point_dist(*points_brute(p))) for p in tqdm(dataset)]
# smart = [timer(lambda:point_dist(*points_smart(p))) for p in tqdm(dataset)]

# plt.plot(np.log(dumb), label="dumb")
# plt.plot(np.log(smart), label="smart!")

# plt.legend()
# plt.show()
