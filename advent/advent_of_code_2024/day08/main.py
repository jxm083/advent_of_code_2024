from math import sqrt
from typing import TypeAlias, Iterator, Callable
from functools import partial
from itertools import count
from pathlib import Path

from advent.common.data_stream import stream_lines_from_file

DATA_DIR = Path(__file__).parent
EXAMPLE_DATA_PATH = DATA_DIR / "data_example.txt"
DATA_PATH_01 = DATA_DIR / "data_01.txt"

CharData: TypeAlias = tuple[int, int, str]


def stream_position_and_char(
    file_data: Iterator[str],
) -> Iterator[CharData]:  # TODO: move this to common
    for line_num, line in enumerate(file_data):
        for char_num, char in enumerate(line):
            yield (line_num, char_num, char)


def add_tuple(tuple0: tuple[int, ...], tuple1: tuple[int, ...]) -> tuple[int, ...]:
    return tuple([a + b for a, b in zip(tuple0, tuple1)])


def negate_tuple(my_tuple: tuple[int, ...]) -> tuple[int, ...]:
    return tuple([-a for a in my_tuple])


def tuple_displacement(
    tuple0: tuple[int, ...], tuple1: tuple[int, ...]
) -> tuple[int, ...]:
    return add_tuple(tuple1, negate_tuple(tuple0))


def mul_tuple(factor: int, my_tuple: tuple[int, ...]) -> tuple[int, ...]:
    return tuple([factor * a for a in my_tuple])


def distance(point0: tuple[int, int], point1: tuple[int, int]) -> float:
    return sqrt((point1[1] - point0[1]) ** 2 + (point1[0] - point0[0]) ** 2)


# better calc_antinode_pair
def calc_antinode_pair(
    position0: tuple[int, ...], position1: tuple[int, ...]
) -> Iterator[tuple[int, ...]]:
    displacement_01 = tuple_displacement(position0, position1)

    antinode0 = [pos + 2 * dis for pos, dis in zip(position0, displacement_01)]
    antinode1 = [pos - dis for pos, dis in zip(position0, displacement_01)]

    antinode_positions = map(tuple, [antinode0, antinode1])
    for antinode in antinode_positions:
        yield antinode


def diverging_count() -> Iterator[int]:
    for n in count():
        if n % 2 == 0:
            yield n // 2

        else:
            yield -((n - 1) // 2 + 1)


def antinodes_with_resonance(
    antenna0_position: tuple[int, ...], antenna1_position: tuple[int, ...]
) -> Iterator[tuple[int, ...]]:
    displacement = tuple_displacement(antenna0_position, antenna1_position)

    for n in diverging_count():
        yield add_tuple(antenna0_position, mul_tuple(n, displacement))


def position_in_map(
    position: tuple[int, int], num_map_lines: int, num_map_cols: int
) -> bool:
    in_map: bool = False
    if 0 <= position[0] < num_map_lines and 0 <= position[1] < num_map_cols:
        in_map = True

    return in_map


def find_all_antinodes(
    pos_char_stream: Iterator[CharData],
    antinode_func: Callable[
        [tuple[int, ...], tuple[int, ...]], Iterator[tuple[int, ...]]
    ],
) -> list[tuple[int, int]]:
    antenna_positions: dict[str, list[tuple[int, int]]] = dict()
    antinode_positions: list[tuple[int, int]] = list()

    positions_of_characters: list[CharData] = list(pos_char_stream)
    max_line_num = max([line_num for line_num, _, _ in positions_of_characters])
    max_col_num = max([col_num for _, col_num, _ in positions_of_characters])

    position_in_current_map = partial(
        position_in_map, num_map_lines=max_line_num + 1, num_map_cols=max_col_num + 1
    )

    for line_num, col_num, char in positions_of_characters:
        current_position = (line_num, col_num)

        if char != ".":
            if char not in antenna_positions:
                antenna_positions[char] = [current_position]
            else:
                for position in antenna_positions[char]:
                    num_excluded_positions = 0
                    for antinode_position in antinode_func(current_position, position):
                        if num_excluded_positions > 2:
                            break
                        elif position_in_current_map(antinode_position):  # type: ignore
                            antinode_positions.append(antinode_position)  # type: ignore
                        else:
                            num_excluded_positions += 1

                antenna_positions[char].append(current_position)

    filtered_positions = list(filter(position_in_current_map, set(antinode_positions)))

    return filtered_positions


def exercise_one(file_path: Path = DATA_PATH_01):
    file_data = stream_lines_from_file(file_path)
    pos_char_stream = stream_position_and_char(file_data)
    return len(find_all_antinodes(pos_char_stream, calc_antinode_pair))


def exercise_two(file_path: Path = DATA_PATH_01) -> int:
    file_data = stream_lines_from_file(file_path)
    pos_char_stream = stream_position_and_char(file_data)
    return len(find_all_antinodes(pos_char_stream, antinodes_with_resonance))


if __name__ == "__main__":
    print(f"exercise one: {exercise_one()}")
    print(f"exercise two: {exercise_two()}")
