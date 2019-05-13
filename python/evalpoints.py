from closestpoints import PointsFeatureExtractor, points_brute, points_smart, random_points
from linreg import LinOptimizer
from lhyra import Lhyra, Solver, DataGenerator
from time import time
from tqdm import tqdm
from random import randint, random

import numpy as np
from matplotlib import pyplot as plt

PERCENT_SORTED = 0.2

data = lambda length: DataGenerator(lambda: random_points(length))

solvers = [
    Solver(points_smart, []),
    Solver(points_brute, [])
]

sf = PointsFeatureExtractor()
lhyra = Lhyra(solvers, data(1000), sf, LinOptimizer)

lhyra.train(iters=10, sample=10)

print('Lhyra parameters: [m,i,q]')

for s in range(len(solvers)):
    print(lhyra.optimizer.regr[s].coef_, lhyra.optimizer.regr[s].intercept_)

print(lhyra.optimizer.coeffs)
print(lhyra.optimizer.intercepts)

lengths = list(.5*n for n in range(2,20))

def bench(length=100, size=200, fx_normalize=False):
    dg = data(length)
    ex = dg.get_data(size)
    ex2 = [x[:] for x in ex]
    
    times = []

    total_time = 0
    lhyra.clear()

    start = time()
    lh, overhead = lhyra.eval(ex[0])
    total_time += lhyra.times[0]
    for i in tqdm(range(1,size)):
        lhyra.clear()
        lh, overhead = lhyra.eval(ex[i])
        total_time += lhyra.times[0]

    times.append(time()-start)
    times.append(total_time)
    print("Lhyra Time:", time() - start)
    print("Lhyra Quick Time", total_time)
    
    start = time()

    smart_hook = lambda t: points_smart(t, smart_hook)
    for i in tqdm(range(size)):
        points_smart(ex[i], smart_hook)

    times.append(time()-start)
    print("Smart time:", time()-start)
    start = time()

    for i in tqdm(range(size)):
        points_brute(ex[i], None)

    times.append(time()-start)
    print("Brute time:", time()-start)

    assert(ex == ex2) # Confirming no side effects
    
    return tuple(times)

alltimes = []
labels = ['Lhyra', 'Lhyra Quick', 'Smart', 'Brute']
for l in lengths:
    alltimes.append(bench(length=int(2**l)))
t = np.array(alltimes).T
for i in range(t.shape[0]):
    plt.plot(lengths, np.log(t[i]), label=labels[i])
plt.legend()
plt.show()