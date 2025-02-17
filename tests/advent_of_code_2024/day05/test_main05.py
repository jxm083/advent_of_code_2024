import pytest

from pathlib import Path

from advent.advent_of_code_2024.day05.main import (
    exercise_one,
    compile_rule_dict,
    stream_rules,
    valid_page_list,
    parse_list,
    exercise_two,
    reorder_pages,
    is_page_list
)
import advent.advent_of_code_2024.day05.main as test_script # TODO: best way to get path reference?
from advent.common.data_stream import stream_lines_from_file

DATA_DIR = Path(test_script.__file__).parent
DATA_EXAMPLE_ONE = DATA_DIR / "data_example_1.txt"

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

def test_stream_rules():
    stream = stream_rules("48|53")
    assert list(stream)[0] == (48, 53)

def test_compile_rule_dict(example_one_rules: dict[int, list[int]]):
    assert compile_rule_dict(DATA_EXAMPLE_ONE) == example_one_rules

def test_is_page_list():
    test_list_text = "75,29,13"
    assert is_page_list(test_list_text) is True

    test_rule_text = "48|53"
    assert is_page_list(test_rule_text) is False

    file_stream = stream_lines_from_file(DATA_EXAMPLE_ONE)

    lists_stream = filter(is_page_list, file_stream)
    assert len([text for text in lists_stream]) > 0

def test_parse_list():
    test_list_text = "75,29,13"
    assert parse_list(test_list_text) == [75, 29, 13]

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