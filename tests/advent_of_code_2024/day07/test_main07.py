from pathlib import Path
from typing import Iterator

import pytest

from advent.advent_of_code_2024.day07.main import (
    parse_equation,
    exercise_one
)

@pytest.fixture
def example_data() -> Iterator[str]:
    data = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

    return iter(data.splitlines())


@pytest.fixture
def example_data_file(tmp_path: Path, example_data: list[str]):
    fake_file = tmp_path / "day07_example_data.txt"
    data = "\n".join(line for line in example_data)
    fake_file.write_text(data)
    return fake_file


def test_parse_equation(example_data: list[str]): # TODO: cast by typing?
    assert example_data[0] == (190, (10, 19))

def test_exercise_one_example(example_data_file: Path):
    assert exercise_one(example_data_file) == 3749