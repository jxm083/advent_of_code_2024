from typing import TypeVar
from dataclasses import dataclass

T = TypeVar('T')

@dataclass(frozen=True)
class Vector(list[int]):
    components: list[int]
    def length(self) -> int:
        return sum(n * n for n in self.components)

def vec_add(vec0: Vector, vec1: Vector) -> Vector:
    return Vector([x + y for x, y in zip(vec0.components, vec1.components)])

def vec_mul(fac: int, vec: Vector) -> Vector:
    return Vector([fac * x for x in vec.components])

def vec_dot(vec0: Vector, vec1: Vector) -> int:
    return sum(x * y for x, y in zip(vec0.components, vec1.components))



