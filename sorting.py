from typing import Any, Callable, Dict, List
from lhyra import Solver, FeatureExtractor
from math import log2
from random import random


def random_list(max_length: int=1000):
    """
    Create a random list of values between 0 and 1 of lengths
    between and max_length.
    :param max_length: The maximum size of list to be generated.
    :return: The generated list.
    """

    return [random() for _ in range(max_length)]


class SortFeatureExtractor(FeatureExtractor):
    @property
    def shape(self) -> List[int]:
        """
        Get the output shape of the feature extractor.
        :return: A list of integers representing the output's dimensions.
        """
        return [1] # Length, (mean, variance)?

    def __call__(self, data: Any) -> List:
        """
        Call extractor on given data.
        :param data: A piece of data to extract the parameters of.
        :return: Floats between 0 and 1 of shape self.shape.
        """
        return [1/(log2(len(data)+2))]

        
def merge_sort(data: List, hook: Callable, _: Dict[str, Any]) -> List:
    """
    :param data: The list to be sorted.
    :param hook: The function used for recursive calls.
    :param _: Unused parameters.
    :return: A sorted list.
    """
    if len(data) == 1:
        return data

    sorted_first = hook(data[:len(data)//2])
    sorted_second = hook(data[len(data)//2:])

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

    return joined


def insertion_sort(data: List, hook: Callable, _: Dict[str, Any]) -> List:
    """
    :param data: The list to be sorted.
    :param hook: The function used for recursive calls.
    :param _: Unused parameters.
    :return: A sorted list.
    """
    if len(data) == 1:
        return data[:]
        
    sorted_data = data[:]

    for i in range(len(sorted_data)-1):
        j = i
        while j >= 0 and sorted_data[j+1] < sorted_data[j]:
            temp = sorted_data[j]
            sorted_data[j] = sorted_data[j+1]
            sorted_data[j+1] = temp
            j -= 1
            
    return sorted_data


# Taken from https://www.geeksforgeeks.org/quick-sort/
def quick_sort(data: List, hook: Callable, _: Dict[str, Any]):
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
    if len(p_data) <= 1: return p_data
    pi = partition(p_data)
    return hook(p_data[:pi])+[p_data[pi]]+hook(p_data[pi+1:])
    
    
    
# Poor man's unit testing
if __name__ == '__main__':
    from time import time

    merge_hook = lambda t: merge_sort(t, merge_hook, None)
    insertion_hook = lambda t: insertion_sort(t, None, None)
    quick_hook = lambda t: quick_sort(t, quick_hook, None)
    
    print(quick_sort([8,7,6,5,4,3,2,1], quick_hook, None))
    
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
    print('All tests passed in', time()-t)
