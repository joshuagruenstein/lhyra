from sorting import SortFeatureExtractor, merge_sort, radix_sort, insertion_sort, quick_sort, random_list
from qlearn import ValueOptimizer
from lhyra import Lhyra, Solver, DataGenerator
from time import time

data = DataGenerator(lambda: sorted(random_list()))

solvers = [
    Solver(merge_sort, []),
    Solver(insertion_sort, []),
    Solver(quick_sort, [])
]

lhyra = Lhyra(solvers, data, SortFeatureExtractor(), ValueOptimizer)

lhyra.train(iters=1000)

def bench():
    ex = sorted(random_list())

    start = time()

    py = sorted(ex)

    print("Py time:", time()-start)
    start = time()

    lh = lhyra.eval(ex, vocal=True)

    print("Lhyra time:", time()-start)
    start = time()

    merge_hook = lambda t: merge_sort(t, merge_hook, None)
    merge_sort(ex, merge_hook, None)

    print("Merge time:", time()-start)
    start = time()

    insert_hook = lambda t: insertion_sort(t, insert_hook, None)
    insertion_sort(ex, insert_hook, None)

    print("Insertion time:", time()-start)
    start = time()

    quick_hook = lambda t: quick_sort(t, quick_hook, None)
    quick_sort(ex, quick_hook, None)

    print("Quick time:", time()-start)
    start = time()

    radix_hook = lambda t: radix_sort(t, radix_hook, None)
    radix_sort(ex, radix_hook, None)

    print("Radix time:", time()-start)

bench()