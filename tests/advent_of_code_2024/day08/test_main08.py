import pytest
from typing import Iterator
from math import sqrt

from advent.advent_of_code_2024.day08.main import (
    distance,
    stream_position_and_char,
    exercise_one
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

def test_stream_position_and_char(example_data: Iterator[str]):
    example_antenna_data = [
        (1, 8, "0"),
        (2, 5, "0"),
        (3, 7, "0"),
        (4, 4, "0"),
        (5, 6, "A"),
        (8, 8, "A"),
        (9, 9, "A")
    ]
    data = stream_position_and_char(example_data)
    # a happy-path test of the stream, looking at only
    # a subset of the data
    def filter_periods(datum: tuple[int, int, str]) -> bool:
        return datum[2] != "."

    assert list(
        filter(
            filter_periods, 
            [datum for datum in data]
            )
            ) == example_antenna_data

def test_distance():
    assert distance((0, 0), (2, 2)) == sqrt(8)

def test_exercise_one():
    assert exercise_one() == 14