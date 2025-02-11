import pytest

from pathlib import Path

from advent.advent_of_code_2024.day05.main import (
    exercise_one,
    import_rules,
    import_draft_page_lists,
    parse_rule
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
def example_one_draft_page_lists() -> list[list[int]]:
    return [
        [75, 47, 61, 53, 29],
        [97, 61, 53, 29, 13],
        [75, 29, 13],
        [75, 97, 47, 61, 53],
        [61, 13, 29],
        [97, 13, 75, 29, 47]
    ]

def test_parse_rule():
    assert parse_rule("47|53") == (47, 53)

def test_import_rules(example_one_rules: dict[int, list[int]]):
    assert import_rules(DATA_EXAMPLE_ONE) == example_one_rules

def test_import_draft_page_lists(example_one_draft_page_lists: list[list[int]]):
    assert import_draft_page_lists(DATA_EXAMPLE_ONE) == example_one_draft_page_lists

def test_exercise_one_example():
    assert exercise_one(DATA_EXAMPLE_ONE) == 143