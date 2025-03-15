from collections.abc import Sequence
from typing import TypeVar, Union, overload

T = TypeVar("T")


class Vector(tuple[int, ...]):
    def __add__(self, other: tuple[int, ...]) -> "Vector":
        return Vector([x + y for x, y in zip(self, other)])

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector([x - y for x, y in zip(self, other)])

    @overload
    def __mul__(self, other: int) -> "Vector": ...
    @overload
    def __mul__(self, other: tuple[int, ...]) -> "Vector": ...

    def __mul__(self, other):
        if isinstance(other, int):
            return Vector([other * x for x in self])
        elif isinstance(other, "Vector"):
            return Vector([x * y for x, y in zip(self, other)])
        else:
            raise ValueError("Not a valid comparison")

    def __rmul__(self, other: Union["Vector", int]):  # type: ignore
        if isinstance(other, int):
            return Vector([other * x for x in self])
        else:
            return Vector([x * y for x, y in zip(self, other)])

    def __eq__(self, other: "Vector"):  # type: ignore
        equal = True
        for x, y in zip(self, other):
            if x != y:
                equal = False

        return equal

    # def __hash__(self):  # type:ignore
    #     return hash(tuple(self.components))

    def __neg__(self):
        return Vector([-x for x in self])

    def dot(self, other: Sequence[int]) -> int:
        return sum(x * y for x, y in zip(self, other))

    def magnitude(self) -> int:
        return sum(n * n for n in self)
