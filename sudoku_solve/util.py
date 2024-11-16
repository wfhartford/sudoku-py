from typing import TypeVar

T = TypeVar("T")

def single(l: list[T]) -> T:
    if len(l) == 0:
        raise RuntimeError("List is empty")
    elif len(l) > 1:
        raise RuntimeError("List has more than one element")
    else:
        return l[0]
