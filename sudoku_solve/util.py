from typing import TypeVar

T = TypeVar("T")

def single(l: list[T]) -> T:
    """
    Returns the only element from a list. If there are no elements, or more than one element a `RuntimeError` is thrown.
    :param l: The list
    :return: The only element in `l`
    """
    if len(l) == 0:
        raise RuntimeError("List is empty")
    elif len(l) > 1:
        raise RuntimeError("List has more than one element")
    else:
        return l[0]
