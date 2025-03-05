from math import sqrt
from typing import TypeAlias, Iterator
from functools import partial
from pathlib import Path

from advent.common.data_stream import stream_lines_from_file

DATA_DIR = Path(__file__).parent
EXAMPLE_DATA_PATH = DATA_DIR / "data_example.txt"
DATA_PATH_01 = DATA_DIR / "data_01.txt"

CharData: TypeAlias = tuple[int, int, str]
def stream_position_and_char(file_data: Iterator[str]) -> Iterator[CharData]: # TODO: move this to common
    for line_num, line in enumerate(file_data):
        for char_num, char in enumerate(line):
            yield (line_num, char_num, char)

def distance(point0: tuple[int, int], point1: tuple[int, int]) -> float:
    return sqrt((point1[1] - point0[1]) ** 2 + (point1[0] - point0[0]) ** 2)

# better calc_antinode_pair
def calc_antinode_pair(position0: tuple[int, ...], position1: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    displacement_01 = [b - a for a, b in zip(position0, position1)]
    antinode0 = [pos + 2 * dis for pos, dis in zip(position0, displacement_01)]
    antinode1 = [pos - dis for pos, dis in zip(position0, displacement_01)]
    return tuple(antinode0), tuple(antinode1)

def position_in_map(position: tuple[int, int], num_map_lines: int, num_map_cols: int) -> bool:
    in_map: bool = False
    if 0 <= position[0] < num_map_lines and 0 <= position[1] < num_map_cols:
        in_map = True
    
    return in_map

def find_all_antinodes(pos_char_stream: Iterator[CharData]) -> list[tuple[int, int]]:
    antenna_positions: dict[str, list[tuple[int, int]]] = dict()
    antinode_positions: list[tuple[int, int]] = list()
    
    max_col_num = 0
    max_line_num = 0
    for line_num, col_num, char in pos_char_stream:
        max_line_num = line_num
        max_col_num = max(col_num, max_col_num)
        if char != ".":
            if char not in antenna_positions:
                antenna_positions[char] = [(line_num, col_num)]
            else:
                for position in antenna_positions[char]:
                    for antinode_position in calc_antinode_pair((line_num, col_num), position):
                        antinode_positions.append(antinode_position) # type:ignore

    position_in_current_map = partial(
        position_in_map, num_map_lines=max_line_num, num_map_cols=max_col_num
    )
    
    filtered_positions = list(filter(
        position_in_current_map, set(antinode_positions)
    ))

    print(filtered_positions)
    return filtered_positions

def exercise_one(file_path: Path = DATA_PATH_01):
    file_data = stream_lines_from_file(file_path)
    pos_char_stream = stream_position_and_char(file_data)
    return len(find_all_antinodes(pos_char_stream))

if __name__ == "__main__":
    print(f"exercise one: {exercise_one(EXAMPLE_DATA_PATH)}")