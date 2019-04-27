from typing import Any, Callable, Dict, List
from lhyra import Solver, FeatureExtractor
from math import log2


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
        return 1/(log2(len(data))+1)

        
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
        return data
        
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
    def partition(data, low, high):
        # pivot (Element to be placed at right position)
        pivot = data[high]
        i = low  # Index of smaller element
        for j in range(low, high):
            if data[j] <= pivot:
                temp = data[i]
                data[i] = data[j]
                data[j] = temp
                i += 1
        temp = data[i+1]
        data[i+1] = data[high]
        data[high] = temp
        return (i + 1)
        
    pi = partition(data, 0, len(data)-1)
    print(data)
    return hook(data[:pi-1])+[data[pi]]+hook(data[pi+1:])
    
# Poor man's unit testing
if __name__ == '__main__':
    merge_hook = lambda t: merge_sort(t, merge_hook, None)
    insertion_hook = lambda t: insertion_sort(t, None, None)
    
    print(quick_sort([8,7,6,5,4,3,2,1], merge_hook, None))
    
    from random import shuffle, randint
    
    for test in range(10):
        test_list = list(range(randint(3,1000)))
        expected = sorted(test_list)
    
        assert(insertion_sort(test_list, None, None) == expected)
        assert(merge_sort(test_list, merge_hook, None) == expected)
        assert(merge_sort(test_list, insertion_hook, None) == expected)
    print('All tests passed')
    