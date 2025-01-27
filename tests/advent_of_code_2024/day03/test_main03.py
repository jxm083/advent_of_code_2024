import pytest

from advent.advent_of_code_2024.day03.main import (
    exercise_one,
    line_to_funcs
) 

from pathlib import Path

@pytest.fixture
def test_line() -> str:
    line = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    return line

@pytest.fixture
def test_data_file(
        test_line: str,
        tmp_path: Path
) -> Path:
    line: str = test_line

    fake_path = tmp_path / "fake.txt"
    fake_path.write_text(line)

    return fake_path

def test_line_to_funcs(test_line: str):
    answer: list[str] = [
        "mul(2,4)",
        "mul(5,5)",
        "mul(11,8)",
        "mul(8,5)"
    ]
    assert line_to_funcs(test_line) == answer

def test_exercise_one():
    assert exercise_one() == 161