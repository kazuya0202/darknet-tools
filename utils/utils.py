
def has_elems_in_list(_list, elms):
    """ リスト内に要素が含まれているかどうか """
    if isinstance(_list, list) or isinstance(_list, tuple):
        res = [True if elm in _list else False for elm in elms]
        return any(res)

    return elms in _list
