import pytest

from pathlib import Path

from advent.advent_of_code_2024.day04.main import (
    generate_text_block,
    exercise_one,
    convert_lines_to_grid,
    cut_line_from_grid,
    cuts_at_letter,
    exercise_two
)

PACKAGE_ROOT_LEVEL = 3
ROOT_PACKAGE_DIR = Path(__file__).parents[PACKAGE_ROOT_LEVEL]
DATA_DIR = ROOT_PACKAGE_DIR / "advent" / "advent_of_code_2024" / "day04"
DATA_TEST = DATA_DIR / "data00.txt"

def test_generate_text_block():
    assert generate_text_block(DATA_TEST, 2) == ['MMMSXXMASM\n', 'MSAMXMSMSA\n']

@pytest.fixture
def fake_text_lines() -> list[str]:
    return [
        "ABC",
        "DEF",
        "GHI"
    ]

@pytest.fixture
def fake_grid() -> list[list[str]]:
    grid = [
            ["A", "B", "C"],
            ["D", "E", "F"],
            ["G", "H", "I"]
        ]
    return grid

def test_convert_lines_to_grid(fake_text_lines: list[str], fake_grid: list[list[str]]):
    assert convert_lines_to_grid(fake_text_lines) == fake_grid

def test_cut_line_from_grid(fake_grid: list[list[str]]):
    length: int = 3
    direct: tuple[int, int] = (1, 1)
    assert cut_line_from_grid(fake_grid, length, direct) == ["A", "E", "I"]

    direct = (0, 1)
    center: tuple[int, int] = (1, 0)
    assert cut_line_from_grid(fake_grid, length, direct, center=center) == ["B", "E", "H"]

    direct = (-1, 0)
    center = (2, 0)
    assert cut_line_from_grid(fake_grid, length, direct, center=center) == ["C", "B", "A"]

def test_cuts_at_letter(fake_grid: list[list[str]]):
    assert cuts_at_letter(fake_grid, 0, 3) == [
        ["A", "B", "C"],
        ["A", "E", "I"],
        ["A", "D", "G"]
    ]

    assert cuts_at_letter(fake_grid, 2, 3) == [
        ["C", "F", "I"],
        ["C", "E", "G"]
    ]

def test_exercise_one_example():
    assert exercise_one(DATA_DIR / "data00.txt") == 18

def test_exercise_one_real():
    assert exercise_one() == 2639

def test_exercise_two_example():
    assert exercise_two(DATA_DIR / "data00.txt") == 9