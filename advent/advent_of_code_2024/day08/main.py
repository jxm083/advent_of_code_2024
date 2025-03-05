from math import sqrt
from typing import TypeAlias, Iterator

CharData: TypeAlias = tuple[int, int, str]
def stream_position_and_char(file_data: Iterator[str]) -> Iterator[CharData]: # TODO: move this to common
    for line_num, line in enumerate(file_data):
        for char_num, char in enumerate(line):
            yield (line_num, char_num, char)

def distance(point0: tuple[int, int], point1: tuple[int, int]) -> float:
    return sqrt((point1[1] - point0[1]) ** 2 + (point1[0] - point0[0]) ** 2)

# better calc_antinode_pair
def antinode_positions(position0: tuple[int, ...], position1: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    displacement_01 = [b - a for a, b in zip(position0, position1)]
    antinode0 = [pos + 2 * dis for pos, dis in zip(position0, displacement_01)]
    antinode1 = [pos - dis for pos, dis in zip(position0, displacement_01)]
    return tuple(antinode0), tuple(antinode1)

def exercise_one():
    pass

if __name__ == "__main__":
    print(f"exercise one: {exercise_one()}")