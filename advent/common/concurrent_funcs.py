from concurrent.futures import ProcessPoolExecutor

from functools import partial
from typing import TypeVar, Callable, Iterator

T = TypeVar('T')
U = TypeVar('U')

def filter_pair(candidate: T, filter_func: Callable[[T], bool]) -> tuple[T, bool]:
    return candidate, filter_func(candidate)

#  modified from https://stackoverflow.com/a/57838062
def pool_filter(
        pool: ProcessPoolExecutor, 
        filter_func: Callable[[T], bool], candidates: Iterator[T]) -> Iterator[T]:
    filter_pair_temp = partial(filter_pair, filter_func=filter_func)
    return (c for c, keep in pool.map(filter_pair_temp, candidates) if keep)
