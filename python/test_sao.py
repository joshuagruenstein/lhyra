from sorting import SortFeatureExtractor, merge_sort, insertion_sort, quick_sort, radix_sort, random_list
from policy import SAOptimizer
from lhyra import Lhyra, Solver, DataGenerator
from time import time
from tqdm import tqdm
from random import randint

data = DataGenerator(lambda: random_list(randint(50, 5000)))

solvers = [
    Solver(merge_sort, []),
    Solver(insertion_sort, []),
    Solver(quick_sort, []),
    Solver(radix_sort, [])
]

lhyra = Lhyra(solvers, data, SortFeatureExtractor(), SAOptimizer)

lhyra.train(iters=20, sample=20)

def bench():
    ex = data.get_data(200)
    ex2 = [x[:] for x in ex]

    start = time()

    sorted_ex = [sorted(x) for x in ex]

    print("Py time:", time()-start)
    start = time()
    lh = lhyra.eval(ex[0], vocal=True)
    for i in tqdm(range(1,200)):
        lh = lhyra.eval(ex[i], vocal=False)

    print("Lhyra time:", time()-start)
    start = time()

    merge_hook = lambda t: merge_sort(t, merge_hook, None)
    for i in tqdm(range(200)):
        merge = merge_sort(ex[i], merge_hook, None)

    print("Merge time:", time()-start)
    start = time()

    insert_hook = lambda t: insertion_sort(t, insert_hook, None)
    for i in tqdm(range(200)):
        merge = insertion_sort(ex[i], insert_hook, None)

    print("Insertion time:", time()-start)
    start = time()

    quick_hook = lambda t: quick_sort(t, quick_hook, None)
    for i in tqdm(range(200)):
        quick = quick_sort(ex[i], quick_hook, None)

    print("Quick time:", time()-start)
    start = time()

    radix_hook = lambda t: radix_sort(t, radix_hook, None)
    for i in tqdm(range(200)):
        radix = radix_sort(ex[i], radix_hook, None)

    print("Radix time:", time()-start)
    
    assert(ex == ex2) # Confirming no side effects


bench()