from sorting import SortFeatureExtractor, merge_sort, insertion_sort, quick_sort, radix_sort, random_list
from lhyrasort import lhyra_sort
from linreg import LinOptimizer
from lhyra import Lhyra, Solver, DataGenerator
from time import time
from tqdm import tqdm
from random import randint

import numpy as np
from matplotlib import pyplot as plt

data = DataGenerator(lambda: random_list(randint(1000,1000)))

solvers = [
    Solver(merge_sort, []),
    Solver(insertion_sort, []),
    Solver(quick_sort, []) #,
    # Solver(radix_sort, [])
]

sf = SortFeatureExtractor()
lhyra = Lhyra(solvers, data, sf, LinOptimizer)

quicklhyra = Lhyra(solvers, data, sf, LinOptimizer)
#quicklhyra.optimizer.coeffs = np.array([[0,0,0],[0,0,0],[0,0,0]])
#quicklhyra.optimizer.intercepts = np.array([1,1,0])
quicklhyra.optimizer.coeffs = np.array([[0 for n in range(sf.shape[0])] for s in solvers])
quicklhyra.optimizer.intercepts = np.array([1 for s in solvers][:-1]+[0])

lhyra.train(iters=200, sample=20)
#lhyra.optimizer.coeffs = np.array([[  7.02924770e-06, -6.41693631e-07, 1.11454411e-08], 
#             [  2.77095379e-05, -4.98456258e-06, 1.04908416e-07],
#             [  1.52831053e-05, -1.95691895e-06, 2.02251640e-08]]) 
#lhyra.optimizer.intercepts = np.array([1.07302477871e-05, -5.74258092972e-05, -5.38219028179e-06])

#lhyra.optimizer.coeffs = np.array([[  7.95957933e-08  , 3.13214568e-07 ,  7.84754425e-09],
# [  1.17647476e-05,  -2.22052775e-06   ,8.49854700e-08],
# [  1.25715975e-05  ,-1.62537198e-06  , 2.26052259e-08]])
#lhyra.optimizer.intercepts = np.array([  4.55142710e-05 , -2.21855518e-05 , -1.30556964e-05])

print('Lhyra parameters: [m,i,q,r]')
for s in range(len(solvers)):
    print(lhyra.optimizer.regr[s].coef_, lhyra.optimizer.regr[s].intercept_)
    
print(lhyra.optimizer.coeffs)
print(lhyra.optimizer.intercepts)

lengths = list(.5*n for n in range(2,21))


def bench(length=100, size=200, fx_normalize=False):

    if fx_normalize:
        fxdict = { 'fx': sf }
    else:
        fxdict = {}

    dg = DataGenerator(lambda: random_list(randint(length,length)))
    ex = dg.get_data(size)
    ex2 = [x[:] for x in ex]
    
    times = []

    start = time()

    sorted_ex = [sorted(x) for x in ex]

    print("Py time:", time()-start)
    #lh = lhyra.vocal_eval(ex[0])
    total_time = 0
    lhyra.clear()
    lh = lhyra.eval(ex[0])

    start = time()
    total_time += lhyra.times[0]
    for i in tqdm(range(1,size)):
        lhyra.clear()
        lh = lhyra.eval(ex[i])
        total_time += lhyra.times[0]
    # print("Lhyra dumbtime", lhyra.optimizer.totaltime)
    times.append(time()-start)
    times.append(total_time)
    print("Lhyra Time:", start - time())
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
    """
    start = time()

    radix_hook = lambda t: radix_sort(t, radix_hook, fxdict)
    for i in tqdm(range(size)):
        radix = radix_sort(ex[i], radix_hook, fxdict)

    times.append(time()-start)
    print("Radix time:", time()-start)
    start = time()

    # quicklhyra.vocal_eval(ex[0])
    for i in tqdm(range(size)):
        quicklhyra.eval(ex[i])

    times.append(time()-start)
    print("Lhyra-handicapped time:", time()-start)
    start = time()

    for i in tqdm(range(size)):
        sdfdasdf = lhyra_sort(ex[i])
        
    times.append(time()-start)
    print("LhyraSort time:", time()-start)
    """
    
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