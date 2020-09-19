"""Utilizes binary search to enable quick searching of sorted lists and insertion in sorted order. The keyword argument which accepts a funciton object allows for custom comparisons.

Functions:

bin_search(a_list, key_obj, key_func = None) -> int
bin_insert(a_list, key_obj, key_func = None) -> None
"""

def bin_search(a_list: list, key_obj, key_func = None) -> int:
    """ Accepts a sorted or empty list and the item to be searched for within the list, returns the index position.

    If the key is not in the list, it returns the index where that key would be. Utilizes binary search for O(log n) complexity.

     Keyword arguments:
        key_funct -- function which returns comparison value (default None)
    """ 
    if key_func == None:
        key_func = lambda x: x
    key_val = key_func(key_obj)
    
    start_index = 0
    end_index = len(a_list)
    
    while (True):
        mid_index = (start_index + end_index) // 2

        if start_index >= end_index:
            return start_index
        if mid_index > len(a_list):
            return mid_index

        mid_val = key_func(a_list[mid_index])

        if key_val > mid_val:
            start_index = mid_index + 1
        elif key_val < mid_val:
            end_index = mid_index
        elif key_val == mid_val:
            return mid_index

def bin_insert(a_list: list, key_obj, key_func = None) -> None:
    """Inserts object in list in sorted order.

    Keyword arguments:
        key_funct -- function which returns comparison value (default None)
    """
    i = bin_search(a_list, key_obj, key_func)
    a_list.insert(i, key_obj)





