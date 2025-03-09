from itertools import combinations, groupby, starmap
from functools import partial
from pathlib import Path
from typing import Callable, Iterator, TypeAlias, Iterable
from operator import itemgetter

from advent.common.data_stream import (
    stream_lines_from_file,
    stream_position_and_char,
    CharData,
)
from advent.common.extended_itertools import diverging_count, takewhile_pair, flatten

DATA_DIR = Path(__file__).parent
EXAMPLE_DATA_PATH = DATA_DIR / "data_example.txt"
DATA_PATH_01 = DATA_DIR / "data_01.txt"


# TODO: change to Vector class?
Coordinate: TypeAlias = tuple[int, ...]


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


def find_antenna_groups(
    grid_stream: Iterable[CharData],
) -> Iterator[Iterator[Coordinate]]:
    only_antennas_grid = filter(lambda x: x[2] != ".", grid_stream)
    antenna_groups_with_key = groupby(
        sorted(only_antennas_grid, key=itemgetter(2)), itemgetter(2)
    )

    for _, group in antenna_groups_with_key:
        group_coordinates = (x[:2] for x in group)
        yield group_coordinates


# TODO: better find_antinode_pair, maybe using vectors
def find_antinode_pair(
    position0: tuple[int, ...], position1: tuple[int, ...]
) -> Iterator[tuple[int, ...]]:
    displacement_01 = tuple_displacement(position0, position1)

    antinode0 = [pos + 2 * dis for pos, dis in zip(position0, displacement_01)]
    antinode1 = [pos - dis for pos, dis in zip(position0, displacement_01)]

    antinode_positions = map(tuple, [antinode0, antinode1])
    for antinode in antinode_positions:
        yield antinode


def find_antinodes_with_resonance(
    antenna0_position: tuple[int, ...], antenna1_position: tuple[int, ...]
) -> Iterator[tuple[int, ...]]:
    displacement = tuple_displacement(antenna0_position, antenna1_position)

    for n in diverging_count():
        yield add_tuple(antenna0_position, mul_tuple(n, displacement))


def find_antinodes_from_antenna_group(
    antenna_positions: Iterator[Coordinate],
    antinode_func: Callable[
        [Coordinate, Coordinate], Iterator[Coordinate]
    ] = find_antinode_pair,
    in_map: Callable[[Coordinate], bool] = lambda x: True,
) -> Iterator[Coordinate]:
    pairs = combinations(antenna_positions, 2)

    antinodes: list[Coordinate] = []

    for pair in pairs:
        antinodes += takewhile_pair(in_map, antinode_func(*pair))

    return filter(in_map, antinodes)


def create_grid_boundary_filter(
    grid: Iterable[CharData],
) -> Callable[[Coordinate], bool]:
    max_line_index = max([line_ind for line_ind, _, _ in grid])
    max_col_index = max([col_ind for _, col_ind, _ in grid])

    def grid_boundary_filter(position: Coordinate) -> bool:
        in_grid = False
        if 0 <= position[0] <= max_line_index and 0 <= position[1] <= max_col_index:
            in_grid = True

        return in_grid

    return grid_boundary_filter


def find_all_antinodes(
    pos_char_stream: Iterator[CharData],
    antinode_func: Callable[
        [tuple[int, ...], tuple[int, ...]], Iterator[tuple[int, ...]]
    ] = find_antinode_pair,
) -> list[Coordinate]:
    positions_of_characters: list[CharData] = list(pos_char_stream)

    antenna_groups = find_antenna_groups(positions_of_characters)

    position_in_current_map = create_grid_boundary_filter(positions_of_characters)

    find_antinodes_from_antenna_group_partial = partial(
        find_antinodes_from_antenna_group,
        antinode_func=antinode_func,
        in_map=position_in_current_map,
    )

    antinode_positions = flatten(
        find_antinodes_from_antenna_group_partial(group) for group in antenna_groups
    )

    return list(set(antinode_positions))


def count_distinct_antinodes(
    file_path: Path = DATA_PATH_01,
    find_antinode_func: Callable[
        [Coordinate, Coordinate], Iterator[Coordinate]
    ] = find_antinode_pair,
) -> int:
    file_data = stream_lines_from_file(file_path)
    position_char_stream = stream_position_and_char(file_data)

    antinode_count = len(find_all_antinodes(position_char_stream, find_antinode_func))

    return antinode_count


def exercise_one(file_path: Path = DATA_PATH_01):
    return count_distinct_antinodes(
        file_path=file_path, find_antinode_func=find_antinode_pair
    )


def exercise_two(file_path: Path = DATA_PATH_01) -> int:
    return count_distinct_antinodes(
        file_path=file_path, find_antinode_func=find_antinodes_with_resonance
    )


if __name__ == "__main__":
    print(f"exercise one: {exercise_one()}")
    print(f"exercise two: {exercise_two()}")
    file_data = stream_lines_from_file(EXAMPLE_DATA_PATH)
    pos_char_stream = stream_position_and_char(file_data)

    antenna_positions_sorted_by_freq = groupby(
        sorted(filter(lambda x: x[2] != ".", pos_char_stream), key=itemgetter(2)),
        itemgetter(2),
    )

    for key, group in antenna_positions_sorted_by_freq:
        print(key, list(map(lambda x: x[:2], group)))
