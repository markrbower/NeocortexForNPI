from collections import Iterable


def makeIterable(x):  # use `str` in py3.x
    if isinstance(x, Iterable):
        return x
    return [x]

