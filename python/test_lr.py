from sorting import SortFeatureExtractor, merge_sort, insertion_sort, quick_sort, radix_sort, random_list
from lhyrasort import lhyra_sort
from linreg import LinOptimizer
from lhyra import Lhyra, Solver, DataGenerator
from time import time
from tqdm import tqdm
from random import randint, random

import numpy as np
from matplotlib import pyplot as plt

PERCENT_SORTED = 0.2

data = lambda length, p: DataGenerator(lambda: random_list(length) if random()>p else sorted(random_list(length)))

solvers = [
    Solver(merge_sort, []),
    Solver(insertion_sort, []),
    Solver(quick_sort, [])
]

sf = SortFeatureExtractor()
lhyra = Lhyra(solvers, data(1000, PERCENT_SORTED), sf, LinOptimizer)

lhyra.train(iters=100, sample=20)

print('Lhyra parameters: [m,i,q]')

for s in range(len(solvers)):
    print(lhyra.optimizer.regr[s].coef_, lhyra.optimizer.regr[s].intercept_)

print(lhyra.optimizer.coeffs)
print(lhyra.optimizer.intercepts)

#lhyra.optimizer.coeffs[1,1] = -1000000000000

lengths = list(.5*n for n in range(2,24))

def bench(length=100, size=200, fx_normalize=False):

    if fx_normalize:
        fxdict = { 'fx': sf }
    else:
        fxdict = {}

    dg = data(length, PERCENT_SORTED)
    ex = dg.get_data(size)
    ex2 = [x[:] for x in ex]
    
    times = []

    start = time()

    sorted_ex = [sorted(x) for x in ex]

    print("Py time:", time()-start)
    #lh = lhyra.vocal_eval(ex[0])
    total_time = 0
    lhyra.clear()

    start = time()
    lh, overhead = lhyra.eval(ex[0])
    total_time += lhyra.times[0]
    for i in tqdm(range(1,size)):
        lhyra.clear()
        lh, overhead = lhyra.eval(ex[i])
        total_time += lhyra.times[0]
    # print("Lhyra dumbtime", lhyra.optimizer.totaltime)
    times.append(time()-start)
    times.append(total_time)
    print("Lhyra Time:", time() - start)
    print("Lhyra Quick Time", total_time)
    
    start = time()

    merge_hook = lambda t: merge_sort(t, merge_hook, fxdict)
    for i in tqdm(range(size)):
        merge = merge_sort(ex[i], merge_hook, fxdict)

    times.append(time()-start)
    print("Merge time:", time()-start)
    start = time()

    insert_hook = lambda t: insertion_sort(t, insert_hook, fxdict)
    for i in tqdm(range(size)):
        merge = insertion_sort(ex[i], insert_hook, fxdict)

    times.append(time()-start)
    print("Insertion time:", time()-start)
    start = time()

    quick_hook = lambda t: quick_sort(t, quick_hook, fxdict)
    for i in tqdm(range(size)):
        quick = quick_sort(ex[i], quick_hook, fxdict)

    times.append(time()-start)
    print("Quick time:", time()-start)

    assert(ex == ex2) # Confirming no side effects
    
    return tuple(times)

alltimes = []
labels = ['Lhyra', 'Lhyra Quick', 'Merge', 'Insertion', 'Quick']
for l in lengths:
    alltimes.append(bench(length=int(2**l)))
t = np.array(alltimes).T
for i in range(t.shape[0]):
    plt.plot(lengths, np.log(t[i]), label=labels[i])
plt.legend()
plt.show()