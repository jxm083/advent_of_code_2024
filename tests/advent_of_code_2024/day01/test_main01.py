from advent.advent_of_code_2024.day01.main import (
    calc_difference,    
    calc_similiarity
)

TEST_DATA_FILE = "numbers00.csv"

TEST_LIST_A = [3, 4, 2, 1, 3, 3]

TEST_LIST_B = [4, 3, 5, 3, 9, 3]

def test_calc_difference():
    list_a = sorted(TEST_LIST_A)
    list_b = sorted(TEST_LIST_B)

    assert calc_difference(list_a, list_b) == 11

def test_calc_similiarity():
    assert calc_similiarity(TEST_LIST_A, TEST_LIST_B) == 31