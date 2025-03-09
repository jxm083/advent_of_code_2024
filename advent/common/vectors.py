from typing import TypeVar
from dataclasses import dataclass
from collections.abc import Sequence

T = TypeVar('T')

@dataclass(frozen=True)
class Vector(Sequence): # type: ignore
    components: list[int]
    def __len__(self):
        return len(self.components)

    def __getitem__(self, key: slice): # type: ignore
        return self.components[key]

    def __add__(self, other): # type: ignore
        return Vector([x + y for x, y in zip(self.components, other.components)]) # type:ignore

    def __sub__(self, other): # type: ignore
        return Vector([x - y for x, y in zip(self.components, other.components)]) # type: ignore

    def __mul__(self, other): # type: ignore
        if type(other) is int: # type: ignore
            return Vector([other * x for x in self.components])
        else:
            return Vector([x * y for x, y in zip(self.components, other.components)]) # type: ignore

    def __rmul__(self, other): # type: ignore
        if type(other) is int: # type: ignore
            return Vector([other * x for x in self.components])
        else:
            return Vector([x * y for x, y in zip(self.components, other.components)]) # type: ignore

    def __eq__(self, other): # type: ignore
        equal = True
        for x, y in zip(self.components, other.components): # type: ignore
            if x != y:
                equal = False

        return equal

    def __neg__(self):
        return Vector([-x for x in self.components])

    def dot(self, other: Sequence[int]) -> int:
        return sum(x * y for x, y in zip(self.components, other.components)) # type: ignore

    def magnitude(self) -> int:
        return sum(n * n for n in self.components)



