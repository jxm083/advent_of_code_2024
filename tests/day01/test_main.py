import pytest
import sys
print(sys.path)

from .days.day01.main import (
    exercise_one
)
from pathlib import Path

TEST_DATA_FILE = "numbers00.csv"

def test_exercise_one():
    assert exercise_one(TEST_DATA_FILE) == 1