import pytest

from advent.advent_of_code_2024.day03.main import (
    exercise_one,
    exercise_two,
    line_to_funcs,
    evaluate_mul_str
) 

from pathlib import Path

@pytest.fixture
def test_line() -> str:
    line = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    return line

@pytest.fixture
def test_logic_line() -> str:
    line = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
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

def test_line_to_funcs(test_line: str, test_logic_line: str):
    answer: list[str] = [
        "mul(2,4)",
        "mul(5,5)",
        "mul(11,8)",
        "mul(8,5)"
    ]
    assert line_to_funcs(test_line) == answer

    logic_answer: list[str] = [
        "mul(2,4)",
        "don't()",
        "mul(5,5)",
        "mul(11,8)",
        "do()",
        "mul(8,5)"
    ]

    assert line_to_funcs(test_logic_line) == logic_answer

def test_evaluate_mul_str():
    assert evaluate_mul_str("mul(2,4)") == 8

PACKAGE_ROOT_LEVEL = 3
ROOT_PACKAGE_DIR = Path(__file__).parents[PACKAGE_ROOT_LEVEL]
DATA_DIR = ROOT_PACKAGE_DIR / "advent_of_code_2024" / "day03"

print("directory:")
print(DATA_DIR)

def test_exercise_one():
    assert exercise_one("data00.txt", file_dir = DATA_DIR) == 161

    assert exercise_one() == 166630675

def test_exercise_two():
    assert exercise_two("data00b.txt", file_dir = DATA_DIR) == 48

    assert exercise_two() == 93465710