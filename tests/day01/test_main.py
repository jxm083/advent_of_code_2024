import pytest

from days_twenty_four.day01.main import (
    calc_difference,    
    calc_similiarity,
    exercise_one
)
from pathlib import Path

TEST_DATA_FILE = "numbers00.csv"

TEST_LIST_A = [3, 4, 2, 1, 3, 3]

TEST_LIST_B = [4, 3, 5, 3, 9, 3]

def test_calc_difference():
    list_a = sorted(TEST_LIST_A)
    list_b = sorted(TEST_LIST_B)

    assert calc_difference(list_a, list_b) == 11

def test_calc_similiarity():
    assert calc_similiarity(TEST_LIST_A, TEST_LIST_B) == 31

#def test_exercise_one():
#    assert exercise_one(TEST_DATA_FILE) == 11

#def test_exercise_two():
#   assert exercise_two(TEST_DATA_FILE) == 31