from typing import Any, Callable, Dict, List
from lhyra import Solver, FeatureExtractor
from math import log2
from random import random, shuffle, randint


def random_list(length: int=1000, killradix=0, nearlysorted=0):
    """
    Create a random list of values between 0 and 1 of lengths
    between and max_length.
    :param max_length: The maximum size of list to be generated.
    :return: The generated list.
    """
    
    
    def shuffle_slice(a, start, stop):
        i = start
        while (i < stop-1):
            idx = randint(i, stop)
            a[i], a[idx] = a[idx], a[i]
            i += 1

    # Sometimes adds a really big number to slow down radix.
    l = list(range(2,length+2))
    if random() < killradix: l.append(2**randint(10,1000))
    if random() < nearlysorted:
        # Create 8 sections of length 5 which are shuffled:
        for i in range(8):
            start = randint(0, length-6)
            shuffle_slice(l, start, start+5)
        l[0] = 1
    else:
        shuffle(l)
    return l


class SortFeatureExtractor(FeatureExtractor):
    @property
    def shape(self) -> List[int]:
        """
        Get the output shape of the feature extractor.
        :return: A list of integers representing the output's dimensions.
        """
        return [4] # Length, (mean, variance)?

    def __call__(self, data: Any) -> List:
        """
        Call extractor on given data.
        :param data: A piece of data to extract the parameters of.
        :return: Floats between 0 and 1 of shape self.shape.
        """
        if len(data) == 0:
            return [0,0,0,1]
        return [len(data), len(data)*log2(len(data)+1), len(data)**2, data[0] == 1]#, log2(max(data)+2) if len(data)>=1 else 0]


def merge_sort(data: List, hook: Callable, _: Dict[str, Any]) -> List:
    """
    :param data: The list to be sorted.
    :param hook: The function used for recursive calls.
    :param _: Unused parameters.
    :return: A sorted list.
    """

    # Call the feature extractor to normalize times
    if len(_) > 0:
        _['fx'](data)

    if len(data) <= 1: return data, 0

    sorted_first, overhead1 = hook(data[:len(data)//2])
    sorted_second, overhead2 = hook(data[len(data)//2:])

    joined = []

    i = 0
    j = 0
    while i + j < len(data):
        if i == len(sorted_first) or (j != len(sorted_second) and
                                      sorted_first[i] > sorted_second[j]):
            joined.append(sorted_second[j])
            j += 1
        else:
            joined.append(sorted_first[i])
            i += 1

    return joined, overhead1 + overhead2


def insertion_sort(data: List, hook: Callable, _: Dict[str, Any]) -> List:
    """
    :param data: The list to be sorted.
    :param hook: The function used for recursive calls.
    :param _: Unused parameters.
    :return: A sorted list.
    """

    # Call the feature extractor to normalize times
    if len(_) > 0:
        _['fx'](data)

    if len(data) == 1:
        return data[:], 0

    sorted_data = data[:]

    for i in range(len(sorted_data)-1):
        j = i
        while j >= 0 and sorted_data[j+1] < sorted_data[j]:
            temp = sorted_data[j]
            sorted_data[j] = sorted_data[j+1]
            sorted_data[j+1] = temp
            j -= 1

    return sorted_data, 0


# Taken from https://www.geeksforgeeks.org/quick-sort/
def quick_sort(data: List, hook: Callable, _: Dict[str, Any]):

    # Call the feature extractor to normalize times
    if len(_) > 0:
        _['fx'](data)

    # Partitions in-place and returns the appropriate position.
    def partition(data):
        pivot = data[len(data)//2]
        i, j = 0, len(data)-1
        while True:
            while data[i] < pivot:
                i += 1
            while data[j] > pivot:
                j -= 1
            if i >= j: return j

            temp = data[i]
            data[i] = data[j]
            data[j] = temp

    p_data = data[:]
    if len(p_data) <= 1:
        return p_data, 0
    pi = partition(p_data)

    data1, overhead1 = hook(p_data[:pi])
    data2, overhead2 = hook(p_data[pi+1:])
    return data1+[p_data[pi]]+data2, overhead1 + overhead2


def counting_sort(data, mod):
    """
    :param data: The list to be sorted.
    :param mod: exp(index of interest)
    """
    buckets = [[] for _ in range(10)]

    for d in data:
        buckets[d//mod % 10].append(d)

    return sum(buckets, [])


def radix_sort(data: List, hook: Callable, _: Dict[str, Any]) -> List:
    """
    :param data: The list to be sorted.
    :param hook: The function used for recursive calls.
    :param _: Unused parameters.
    :return: A sorted list.
    """

    # Call the feature extractor to normalize times
    if len(_) > 0:
        _['fx'](data)

    if len(data) <= 1: return data, 0

    max_element = max(data)
    mod = 1
    while mod < max_element:
        data = counting_sort(data, mod)
        mod *= 10

    return data, 0


# Poor man's unit testing
if __name__ == '__main__':
    from time import time

    merge_hook, _ = lambda t: merge_sort(t, merge_hook, None)
    insertion_hook, _ = lambda t: insertion_sort(t, None, None)
    quick_hook, _ = lambda t: quick_sort(t, quick_hook, None)
    radix_hook, _ = lambda t: radix_sort(t, radix_sort, None)
    print(radix_sort([8,7,6,5,4,3,2,1], quick_hook, None))
    
    from random import shuffle, randint
    
    t = time()
    for test in range(100):
        test_list = list(range(randint(3,1000)))
        expected = sorted(test_list)
    
        assert(insertion_sort(test_list, None, None) == expected)
        assert(merge_sort(test_list, merge_hook, None) == expected)
        assert(merge_sort(test_list, quick_hook, None) == expected)
        assert(merge_sort(test_list, insertion_hook, None) == expected)
        assert(quick_sort(test_list, quick_hook, None) == expected)
        assert(quick_sort(test_list, merge_hook, None) == expected)
        assert(quick_sort(test_list, insertion_hook, None) == expected)
        assert(radix_sort(test_list, None, None) == expected)

    print('All tests passed in', time()-t)
