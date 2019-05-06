from sorting import SortFeatureExtractor, merge_sort, insertion_sort, quick_sort, radix_sort, random_list
from lhyrasort import lhyra_sort
from linreg import LinOptimizer
from lhyra import Lhyra, Solver, DataGenerator
from time import time
from tqdm import tqdm
from random import randint

import numpy as np

data = DataGenerator(lambda: random_list(randint(40,1000), nearlysorted=0.5))

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

lhyra.train(iters=0, sample=20)

print(quicklhyra.optimizer.coeffs, quicklhyra.optimizer.intercepts)

print('Lhyra parameters: [m,i,q,r]')
for s in range(len(solvers)):
    print(lhyra.optimizer.regr[s].coef_, lhyra.optimizer.regr[s].intercept_)

def bench(size=200, fx_normalize=True):

    if fx_normalize:
        fxdict = { 'fx': sf }
    else:
        fxdict = {}

    ex = data.get_data(size)
    ex2 = [x[:] for x in ex]

    start = time()

    sorted_ex = [sorted(x) for x in ex]

    print("Py time:", time()-start)
    start = time()
    lh = lhyra.vocal_eval(ex[0])
    for i in tqdm(range(1,size)):
        lh = lhyra.eval(ex[i])
    print("Lhyra dumbtime", lhyra.optimizer.totaltime)
    print("Lhyra time:", time()-start)
    start = time()

    merge_hook = lambda t: merge_sort(t, merge_hook, fxdict)
    for i in tqdm(range(size)):
        merge = merge_sort(ex[i], merge_hook, fxdict)

    print("Merge time:", time()-start)
    start = time()

    insert_hook = lambda t: insertion_sort(t, insert_hook, fxdict)
    for i in tqdm(range(size)):
        merge = insertion_sort(ex[i], insert_hook, fxdict)

    print("Insertion time:", time()-start)
    start = time()

    quick_hook = lambda t: quick_sort(t, quick_hook, fxdict)
    for i in tqdm(range(size)):
        quick = quick_sort(ex[i], quick_hook, fxdict)

    print("Quick time:", time()-start)
    start = time()

    radix_hook = lambda t: radix_sort(t, radix_hook, fxdict)
    for i in tqdm(range(size)):
        radix = radix_sort(ex[i], radix_hook, fxdict)

    print("Radix time:", time()-start)
    start = time()

    # quicklhyra.vocal_eval(ex[0])
    for i in tqdm(range(size)):
        quicklhyra.eval(ex[i])

    print("Lhyra-handicapped time:", time()-start)
    start = time()

    for i in tqdm(range(size)):
        sdfdasdf = lhyra_sort(ex[i])
        
    print("LhyraSort time:", time()-start)
    
    assert(ex == ex2) # Confirming no side effects


bench()