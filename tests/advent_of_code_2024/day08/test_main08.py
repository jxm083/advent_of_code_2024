import pytest
from typing import Iterator
from pathlib import Path
from itertools import islice

from advent.common.vectors import Vector
from advent.common.data_stream import CharPosition
from advent.advent_of_code_2024.day08.main import (
    stream_position_and_char,
    find_antenna_groups,
    find_antinode_pair,
    find_all_antinodes,
    find_antinodes_with_resonance,
    create_grid_boundary_filter,
    find_antinodes_from_antenna_group,
    exercise_one,
    exercise_two,
)


@pytest.fixture
def example_data() -> Iterator[str]:
    data = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

    return iter(data.splitlines())


@pytest.fixture
def example_data_file(tmp_path: Path, example_data: Iterator[str]):
    fake_file = tmp_path / "day08_example_data.txt"
    data = "\n".join(line for line in example_data)
    fake_file.write_text(data)
    return fake_file


@pytest.fixture
def example_data_stream(example_data_file: Path):
    return stream_position_and_char(example_data_file)


def test_stream_position_and_char(example_data_stream: Iterator[CharPosition]):
    reference_antenna_data = [
        CharPosition(Vector([1, 8]), "0"),
        CharPosition(Vector([2, 5]), "0"),
        CharPosition(Vector([3, 7]), "0"),
        CharPosition(Vector([4, 4]), "0"),
        CharPosition(Vector([5, 6]), "A"),
        CharPosition(Vector([8, 8]), "A"),
        CharPosition(Vector([9, 9]), "A"),
    ]

    # a happy-path test of the stream, looking at only
    # a subset of the data
    def filter_periods(datum: CharPosition) -> bool:
        return datum.char != "."

    assert (
        list(filter(filter_periods, [datum for datum in example_data_stream]))
        == reference_antenna_data
    )


def test_find_antenna_groups(example_data_stream: Iterator[CharPosition]):
    reference_antenna_data = [
        # Frequency 0 antennas
        [Vector([1, 8]), Vector([2, 5]), Vector([3, 7]), Vector([4, 4])],
        # Frequency A antennas
        [Vector([5, 6]), Vector([8, 8]), Vector([9, 9])],
    ]

    test = find_antenna_groups(example_data_stream)

    for test_group, ref_group in zip(test, reference_antenna_data):
        assert set(list(test_group)) == set(ref_group)


def test_find_antinode_pair():
    # added set so as to not test the order in which
    # the coordinates are returned
    assert set(find_antinode_pair(Vector([1, 8]), Vector([2, 5]))) == set(
        (Vector([0, 11]), Vector([3, 2]))
    )


def test_find_antinodes_with_resonance():
    antenna0_position = Vector([0, 0])
    antenna1_position = Vector([2, 3])

    reference_antinodes = list(
        map(lambda x: Vector(list(x)), [(0, 0), (-2, -3), (2, 3), (-4, -6), (4, 6)])
    )

    calc_antinodes = find_antinodes_with_resonance(
        antenna0_position=antenna0_position, antenna1_position=antenna1_position
    )

    assert list(islice(calc_antinodes, 5)) == reference_antinodes


def test_create_grid_boundary_filter(example_data_stream: Iterator[CharPosition]):
    example_data_list = list(example_data_stream)
    in_map = create_grid_boundary_filter(example_data_list)

    assert in_map(Vector([0, 5])) is True
    assert in_map(Vector([99, 99])) is False


def test_find_antinodes_from_antenna_group(example_data_stream: Iterator[CharPosition]):
    example_data = list(example_data_stream)
    antenna_group_stream = find_antenna_groups(example_data)
    antenna_groups = [list(group) for group in antenna_group_stream]
    in_map = create_grid_boundary_filter(example_data)
    antinodes_from_A = list(
        find_antinodes_from_antenna_group(antenna_groups[1], find_antinode_pair, in_map)
    )

    reference_antinodes = list(
        map(Vector, [[2, 4], [11, 10], [7, 7], [10, 10], [1, 3]])
    )

    assert set(antinodes_from_A) == set(reference_antinodes)


def test_find_all_antinodes(example_data_stream: Iterator[CharPosition]):
    reference_antinode_positions: set[Vector] = set(
        map(
            lambda x: Vector(list(x)),
            [
                (2, 4),
                (11, 10),
                (7, 7),
                (4, 9),
                (2, 10),
                (7, 0),
                (5, 1),
                (0, 6),
                (10, 10),
                (5, 6),
                (3, 2),
                (6, 3),
                (1, 3),
                (0, 11),
            ],
        )
    )

    assert set(find_all_antinodes(example_data_stream)) == reference_antinode_positions


def test_exercise_one_example(example_data_file: Path):
    assert exercise_one(example_data_file) == 14


def test_exercise_one_real():
    assert exercise_one() == 240


def test_exercise_two_example(example_data_file: Path):
    assert exercise_two(example_data_file) == 34


def test_exercise_two_real():
    assert exercise_two() == 955
