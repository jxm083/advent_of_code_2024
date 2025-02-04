# import pytest

from pathlib import Path

from advent.advent_of_code_2024.day04.main import (
    generate_text_block,
    exercise_one
)

PACKAGE_ROOT_LEVEL = 3
ROOT_PACKAGE_DIR = Path(__file__).parents[PACKAGE_ROOT_LEVEL]
DATA_DIR = ROOT_PACKAGE_DIR / "advent" / "advent_of_code_2024" / "day04"
DATA_TEST = DATA_DIR / "data00.txt"

def test_generate_text_block():
    assert generate_text_block(DATA_TEST, 2) == ['MMMSXXMASM\n', 'MSAMXMSMSA\n']

def test_exercise_one_example():
    assert exercise_one(DATA_DIR / "data00.txt") == 18

if __name__ == "__main__":
    print(DATA_TEST.exists)
