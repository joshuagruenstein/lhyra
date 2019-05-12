from sorting import merge_sort, insertion_sort, quick_sort
import numpy as np
from math import log2
"""
coeffs = np.array([[  7.02924770e-06, -6.41693631e-07, 1.11454411e-08], 
             [  2.77095379e-05, -4.98456258e-06, 1.04908416e-07],
             [  1.52831053e-05, -1.95691895e-06, 2.02251640e-08]]) 
intercepts = np.array([1.07302477871e-05, -5.74258092972e-05, -5.38219028179e-06])
"""

coeffs = np.array([[  7.95957933e-08  , 3.13214568e-07 ,  7.84754425e-09],
 [  1.17647476e-05,  -2.22052775e-06   ,8.49854700e-08],
 [  1.25715975e-05  ,-1.62537198e-06  , 2.26052259e-08]])
intercepts = np.array([  4.55142710e-05 , -2.21855518e-05 , -1.30556964e-05])

lhyra_hook = lambda t: lhyra_sort(t) 
def lhyra_sort(data):
    features = np.array([len(data), len(data)*log2(len(data)+1), len(data)**2]) if len(data) > 0 else [0,0,0]
    choice = np.argmin(coeffs @ features + intercepts)
    if choice == 0: return merge_sort(data, lhyra_hook, {})
    elif choice == 1: return insertion_sort(data, lhyra_hook, {})
    else: return quick_sort(data, lhyra_hook, {})
"""
coeffs = np.array([[  1.41278615e-05 , -1.31231425e-06 ,  6.86773299e-09,  -1.50966275e-03],
[ -2.58740136e-05 ,  3.65124088e-06 ,  2.50896971e-08 , -1.79948173e-03] ,
[  1.41002391e-05 , -1.94680931e-06  , 2.07435650e-08 , -1.09403240e-03]]) 
intercepts = np.array([3.76358559105e-05, 0.00032508733845, 8.1364347528e-05])

lhyra_hook = lambda t: lhyra_sort(t) 
def lhyra_sort(data):
    features = [len(data), len(data)*log2(len(data)+1), len(data)**2, data[0] == 1] if len(data) > 0 else [0,0,0,1]
    choice = np.argmin(coeffs @ features + intercepts)
    if choice == 0: return merge_sort(data, lhyra_hook, {})
    elif choice == 1: return insertion_sort(data, lhyra_hook, {})
    else: return quick_sort(data, lhyra_hook, {})
"""

if __name__ == '__main__':
    from random import random
    l = [random() for i in range(10000)]
    lhyra_sort(l)