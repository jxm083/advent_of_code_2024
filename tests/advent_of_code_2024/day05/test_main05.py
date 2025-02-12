import pytest

from pathlib import Path

from advent.advent_of_code_2024.day05.main import (
    exercise_one,
    import_rules,
    import_page_lists,
    parse_rule,
    valid_page_list,
    exercise_two,
    reorder_pages
)

PACKAGE_ROOT_LEVEL: int = 3 # TODO: make this better than a relative path
ROOT_PACKAGE_DIR: Path = Path(__file__).parents[PACKAGE_ROOT_LEVEL]
DATA_DIR = ROOT_PACKAGE_DIR / "advent" / "advent_of_code_2024" / "day05"
DATA_EXAMPLE_ONE = DATA_DIR / "data_example_1.txt"

#@pytest.fixture
#def example_one_rules() -> dict[int, list[int]]:
    #return {
        #47: [53, 13, 61, 29],
        #97: [13, 61, 47, 29, 53, 75],
        #75: [29, 53, 47, 61, 13],
        #61: [13, 53, 29],
        #29: [13],
        #53: [29, 13]
    #}

@pytest.fixture
def example_one_rules() -> dict[int, list[int]]:
    return {
        53: [47, 75, 61, 97],
        13: [97, 61, 29, 47, 75, 53],
        61: [97, 47, 75],
        47: [97, 75],
        29: [75, 97, 53, 61, 47],
        75: [97]
    }


@pytest.fixture
def example_one_page_lists() -> list[list[int]]:
    return [
        [75, 47, 61, 53, 29],
        [97, 61, 53, 29, 13],
        [75, 29, 13],
        [75, 97, 47, 61, 53],
        [61, 13, 29],
        [97, 13, 75, 29, 47]
    ]

@pytest.fixture
def example_one_valid_lists() -> list[bool]:
    return [True, True, True, False, False, False]

def test_valid_page_list(
    example_one_rules: dict[int, list[int]],
    example_one_page_lists: list[list[int]],
    example_one_valid_lists: list[bool]
    ):

    valid_list_check: list[bool] = [
        valid_page_list(pages, example_one_rules) for pages in example_one_page_lists
    ]

    assert valid_list_check == example_one_valid_lists # TODO: check comparing boolean lists

def test_parse_rule():
    assert parse_rule("47|53") == (47, 53)

def test_import_rules(example_one_rules: dict[int, list[int]]):
    assert import_rules(DATA_EXAMPLE_ONE) == example_one_rules

def test_import_page_lists(example_one_page_lists: list[list[int]]):
    assert import_page_lists(DATA_EXAMPLE_ONE) == example_one_page_lists

def test_exercise_one_example():
    assert exercise_one(DATA_EXAMPLE_ONE) == 143

def test_exercise_one_real():
    assert exercise_one() == 5129

def test_reorder_pages(
    example_one_page_lists: list[list[int]],
    example_one_rules: dict[int, list[int]]
):
    reordered_pages_list: list[list[int]] = [
        [97, 75, 47, 61, 53],
        [61, 29, 13],
        [97, 75, 47, 29, 13]
    ]

    for ps_good, ps_bad in zip(reordered_pages_list, example_one_page_lists[3:]):
        assert reorder_pages(ps_bad, example_one_rules) == ps_good

def test_exercise_two_example():
    assert exercise_two(DATA_EXAMPLE_ONE) == 123

def test_exercise_two_real():
    assert exercise_two() == 4077