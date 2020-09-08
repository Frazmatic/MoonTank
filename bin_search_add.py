#I can sort by any object characteristic by using keyword arguments and
#passing functions. I needed something that would allow me to perform a
#binary search using those same functions. I also needed it to return the
#index where something *should* go if it's not already in list, so that I
#can keep lists sorted when inserting.
def bin_search(a_list, key_obj, key_func = None):
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

def bin_insert(a_list, key_obj, key_func = None):
    i = bin_search(a_list, key_obj, key_func)
    a_list.insert(i, key_obj)

def search_pieces_list(the_list, coord):

    key_val = (coord.get_x(), coord.get_y())
    
    start_index = 0
    end_index = len(a_list)
    
    while (True):
        mid_index = (start_index + end_index) // 2

        if start_index >= end_index:
            return start_index
        if mid_index > len(a_list):
            return mid_index

        c = a_list[mid_index]
        mid_val = (c.coordinate.get_x(), c.coordinate.get_y())

        if key_val > mid_val:
            start_index = mid_index + 1
        elif key_val < mid_val:
            end_index = mid_index
        elif key_val == mid_val:
            return mid_index



