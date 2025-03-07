from itertools import count
from typing import TypeVar, Iterator, Callable, Iterable

T = TypeVar("T")


def diverging_count() -> Iterator[int]:
    for n in count():
        if n % 2 == 0:
            yield n // 2

        else:
            yield -((n - 1) // 2 + 1)


def takewhile_pair(
    predicate: Callable[[T], bool], iterable: Iterable[T]
) -> Iterator[T]:
    """
    Produces an iterator that does not stop until either two
    sequential items evaluate to false when entered into
    predicate (and these items are excluded)
    or the end of the original iterator is reached.

    e.g. [0, -1, 1, -2, 2, -3, -4] -> [0, -1, 1, -2, 2]
    """
    iterator = iter(iterable)
    last_item: T | None = None

    if last_item is None:
        try:
            last_item = next(iterator)
        except StopIteration:
            return

    for item in iterator:
        if not (predicate(item) or predicate(last_item)):
            break
        else:
            yield last_item

            last_item = item

    if predicate(last_item):
        yield last_item
