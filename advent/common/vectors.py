from typing import TypeVar
from dataclasses import dataclass

T = TypeVar('T')

@dataclass(frozen=True)
class Vector(list[T]):
    def length(self) -> T:
        total_length = self[0]
        for product in (n * n for n in self):

