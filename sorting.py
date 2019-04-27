from typing import Any, Callable, Dict, List

def merge_sort(data: List, hook: Callable, _: Dict[str, Any]) -> List:
    """
    :param data: The list to be sorted.
    :param hook: The function used for recursive calls.
    :param _: Unused parameters.
    :return: A sorted list.
    """
    if len(data) == 1:
        return data

    sorted_first = hook(data[:len(data)/2])
    sorted_second = hook(data[len(data)/2:])

    joined = []

    i = 0
    j = 0
    while i + j < len(joined):
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

    sorted_data = []

    return sorted_data
