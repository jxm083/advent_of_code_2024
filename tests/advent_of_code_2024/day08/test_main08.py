import pytest
from typing import Iterator
from math import sqrt
from pathlib import Path

from advent.advent_of_code_2024.day08.main import (
    distance,
    stream_position_and_char,
    calc_antinode_pair,
    find_all_antinodes,
    exercise_one,
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
def example_data_file(tmp_path: Path, example_data: list[str]):
    fake_file = tmp_path / "day08_example_data.txt"
    data = "\n".join(line for line in example_data)
    fake_file.write_text(data)
    return fake_file


def test_stream_position_and_char(example_data: Iterator[str]):
    reference_antenna_data = [
        (1, 8, "0"),
        (2, 5, "0"),
        (3, 7, "0"),
        (4, 4, "0"),
        (5, 6, "A"),
        (8, 8, "A"),
        (9, 9, "A"),
    ]
    data = stream_position_and_char(example_data)

    # a happy-path test of the stream, looking at only
    # a subset of the data
    def filter_periods(datum: tuple[int, int, str]) -> bool:
        return datum[2] != "."

    assert (
        list(filter(filter_periods, [datum for datum in data]))
        == reference_antenna_data
    )


def test_calc_antinode_pair():
    # added set so as to not test the order in which
    # the coordinates are returned
    assert set(calc_antinode_pair((1, 8), (2, 5))) == set(((0, 11), (3, 2)))


def test_find_all_antinodes(example_data: Iterator[str]):
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

    pos_char_stream = stream_position_and_char(example_data)

    assert set(find_all_antinodes(pos_char_stream)) == reference_antinode_positions


def test_distance():
    assert distance((0, 0), (2, 2)) == sqrt(8)


def test_exercise_one_example(example_data_file: Path):
    assert exercise_one(example_data_file) == 14


def test_exercise_one_real():
    assert exercise_one() == 240
