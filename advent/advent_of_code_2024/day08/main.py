from math import sqrt
from typing import TypeAlias, Iterator

AntennaData: TypeAlias = tuple[int, int, str]
def antenna_data_stream(file_data: Iterator[str]) -> Iterator[AntennaData]: # TODO: move this to common
    for line_num, line in enumerate(file_data):
        for char_num, char in enumerate(line):
            if char != ".":
                yield (line_num, char_num, char)

    

def distance(point0: tuple[int, int], point1: tuple[int, int]) -> float:
    return sqrt((point1[1] - point0[1]) ** 2 + (point1[0] - point0[0]) ** 2)

def exercise_one():
    pass

if __name__ == "__main__":
    print(f"exercise one: {exercise_one()}")