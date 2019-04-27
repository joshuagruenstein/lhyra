from sorting import SortFeatureExtractor, merge_sort, insertion_sort, random_list
from policy import PolicyLinearOptimizer
from lhyra import Lhyra, Solver, DataGenerator
from time import time

data = DataGenerator(random_list)

solvers = [
    Solver(merge_sort, []),
    Solver(insertion_sort, [])
]

lhyra = Lhyra(solvers, data, SortFeatureExtractor(), PolicyLinearOptimizer)

lhyra.train(iters=5)

def bench():
    ex = random_list()[:1000]

    start = time()

    py = sorted(ex)

    print("Py time:", time()-start)
    start = time()

    lh = lhyra.eval(ex)

    print("Lhyra time:", time()-start)
    start = time()

    merge_hook = lambda t: merge_sort(t, merge_hook, None)
    merge = merge_sort(ex, merge_hook, None)

    print("Merge time:", time()-start)
    start = time()

    insert_hook = lambda t: insertion_sort(t, insert_hook, None)
    merge = insertion_sort(ex, insert_hook, None)

    print("Insertion time:", time()-start)

bench()