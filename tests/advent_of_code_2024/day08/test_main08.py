import pytest
from typing import Iterator
from math import sqrt
from pathlib import Path
from itertools import islice, groupby
from operator import itemgetter

from advent.advent_of_code_2024.day08.main import (
    Coordinate,
    CharData,
    distance,
    stream_position_and_char,
    calc_antinode_pair,
    find_all_antinodes,
    add_tuple,
    negate_tuple,
    tuple_displacement,
    mul_tuple,
    diverging_count,
    antinodes_with_resonance,
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
def example_data_stream(example_data: Iterator[str]):
    return stream_position_and_char(example_data)


def test_stream_position_and_char(example_data_stream: Iterator[CharData]):
    reference_antenna_data = [
        (1, 8, "0"),
        (2, 5, "0"),
        (3, 7, "0"),
        (4, 4, "0"),
        (5, 6, "A"),
        (8, 8, "A"),
        (9, 9, "A"),
    ]
    # a happy-path test of the stream, looking at only
    # a subset of the data
    def filter_periods(datum: tuple[int, int, str]) -> bool:
        return datum[2] != "."

    assert (
        list(filter(filter_periods, [datum for datum in example_data_stream]))
        == reference_antenna_data
    )


def test_calc_antinode_pair():
    # added set so as to not test the order in which
    # the coordinates are returned
    assert set(calc_antinode_pair((1, 8), (2, 5))) == set(((0, 11), (3, 2)))


def test_find_all_antinodes(example_data_stream: Iterator[CharData]):
    reference_antinode_positions: set[tuple[int, int]] = set(
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
        ]
    )

    assert set(find_all_antinodes(example_data_stream)) == reference_antinode_positions


def test_distance():
    assert distance((0, 0), (2, 2)) == sqrt(8)


def test_add_tuple():
    assert add_tuple((1, 3), (5, 8)) == (6, 11)
    assert add_tuple((-10, 3), (6, -1)) == (-4, 2)


def test_negate_tuple():
    assert negate_tuple((4, 8)) == (-4, -8)


def test_tuple_displacement():
    assert tuple_displacement((0, 0), (3, 4)) == (3, 4)


def test_mul_tuple():
    assert mul_tuple(5, (2, 11)) == (10, 55)









def test_antinodes_with_resonance():
    antenna0_position = (0, 0)
    antenna1_position = (2, 3)

    reference_antinodes = [(0, 0), (-2, -3), (2, 3), (-4, -6), (4, 6)]

    calc_antinodes = antinodes_with_resonance(
        antenna0_position=antenna0_position, antenna1_position=antenna1_position
    )

    assert list(islice(calc_antinodes, 5)) == reference_antinodes

def test_antinodes_from_antenna_group(example_data_stream: Iterator[CharData]):
    antenna_a_positions = groupby(example_data_stream, itemgetter(2))


def test_exercise_one_example(example_data_file: Path):
    assert exercise_one(example_data_file) == 14


def test_exercise_one_real():
    assert exercise_one() == 240


def test_exercise_two_example(example_data_file: Path):
    assert exercise_two(example_data_file) == 34


def test_exercise_two_real():
    assert exercise_two() == 955
