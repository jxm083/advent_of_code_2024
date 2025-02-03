# import pytest

from pathlib import Path

from advent.advent_of_code_2024.day04.main import (
    exercise_one
)

PACKAGE_ROOT_LEVEL = 3
ROOT_PACKAGE_DIR = Path(__file__).parents[PACKAGE_ROOT_LEVEL]
DATA_DIR = ROOT_PACKAGE_DIR / "advent_of_code_2024" / "day04"

def test_exercise_one_example():
    assert exercise_one(DATA_DIR / "data00.txt") == 18
