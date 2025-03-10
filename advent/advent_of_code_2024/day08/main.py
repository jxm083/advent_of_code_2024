from itertools import combinations, groupby
from functools import partial
from pathlib import Path
from typing import Callable, Iterator, Iterable
from operator import itemgetter

from advent.common.data_stream import (
    stream_position_and_char,
    CharPosition,
)
from advent.common.vectors import Vector
from advent.common.extended_itertools import diverging_count, takewhile_pair, flatten

DATA_DIR = Path(__file__).parent
EXAMPLE_DATA_PATH = DATA_DIR / "data_example.txt"
DATA_PATH_01 = DATA_DIR / "data_01.txt"


def find_antenna_groups(
    grid_stream: Iterable[CharPosition],
) -> Iterator[Iterator[Vector]]:
    only_antennas_grid = filter(lambda x: x.char != ".", grid_stream)
    antenna_groups_with_key = groupby(
        sorted(only_antennas_grid, key=itemgetter(1)), itemgetter(1)
    )

    for _, group in antenna_groups_with_key:
        group_coordinates = (x.position for x in group)
        yield group_coordinates


def find_antinode_pair(
    position0: Vector, position1: Vector
) -> Iterator[Vector]:
    displacement_01 = position1 - position0

    antinode0 = position0 + 2 * displacement_01
    antinode1 = position0 - displacement_01

    antinode_positions = (antinode0, antinode1)
    for antinode in antinode_positions:
        yield antinode


def find_antinodes_with_resonance(
    antenna0_position: Vector, antenna1_position: Vector
) -> Iterator[Vector]:
    displacement = antenna1_position - antenna0_position

    for n in diverging_count():
        yield antenna0_position + n * displacement


def find_antinodes_from_antenna_group(
    antenna_positions: Iterable[Vector],
    antinode_func: Callable[
        [Vector, Vector], Iterator[Vector]
    ] = find_antinode_pair,
    in_map: Callable[[Vector], bool] = lambda x: True,
) -> Iterator[Vector]:
    pairs = combinations(antenna_positions, 2)

    antinodes: list[Vector] = []

    for pair in pairs:
        antinodes += takewhile_pair(in_map, antinode_func(*pair))

    return filter(in_map, antinodes)


def create_grid_boundary_filter(
    grid: Iterable[CharPosition],
) -> Callable[[Vector], bool]:
    max_line_index = max([position[0] for position, _ in grid]) # type: ignore
    max_col_index = max([position[1] for position, _ in grid]) # type: ignore

    def grid_boundary_filter(position: Vector) -> bool:
        in_grid = False
        if 0 <= position[0] <= max_line_index and 0 <= position[1] <= max_col_index: # type: ignore
            in_grid = True

        return in_grid

    return grid_boundary_filter


def find_all_antinodes(
    pos_char_stream: Iterator[CharPosition],
    antinode_func: Callable[
        [Vector, Vector], Iterator[Vector]
    ] = find_antinode_pair,
) -> list[Vector]:
    positions_of_characters: list[CharPosition] = list(pos_char_stream)

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
        [Vector, Vector], Iterator[Vector]
    ] = find_antinode_pair,
) -> int:
    position_char_stream = stream_position_and_char(file_path)

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
    pos_char_stream = stream_position_and_char(EXAMPLE_DATA_PATH)

    antenna_positions_sorted_by_freq = groupby(
        sorted(filter(lambda x: x.char != ".", pos_char_stream), key=itemgetter(1)),
        itemgetter(1),
    )

    duplicates = [Vector([1, 2]), Vector([1, 2])]
    print(set(duplicates))

    for key, group in antenna_positions_sorted_by_freq:
        print(key, list(map(lambda x: x[:2], group)))
