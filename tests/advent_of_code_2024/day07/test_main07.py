from pathlib import Path
from typing import Iterator
from operator import add, mul # TODO import directly or from tested script?

import pytest

from advent.advent_of_code_2024.day07.main import (
    parse_equation,
    generate_function_combo,
    is_valid_equation,
    Equation,
    evaluate_function_combos,
    exercise_one
)

@pytest.fixture
def example_data() -> Iterator[str]:
    data = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

    return iter(data.splitlines())


@pytest.fixture
def example_data_file(tmp_path: Path, example_data: list[str]):
    fake_file = tmp_path / "day07_example_data.txt"
    data = "\n".join(line for line in example_data)
    fake_file.write_text(data)
    return fake_file


def test_parse_equation(example_data: list[str]): # TODO: cast by typing?
    example_data_list: list[str] = [data for data in example_data]
    assert parse_equation(example_data_list[0]) == (190, (10, 19))
    assert parse_equation(example_data_list[1]) == (3267, (81, 40 , 27))

def test_generate_function_combo():
    combos = generate_function_combo(3)
    assert set(combos) == set([
        (add, add),
        (add, mul),
        (mul, add),
        (mul, mul)
    ])

def test_evaluate_function_combos():
    example_terms = (81, 40, 27)
    solutions: list[int] = [148, 3267, 3267, 87480]
    test_solutions = evaluate_function_combos(example_terms)
    assert set(test_solutions) == set(solutions)

def test_is_valid_equation(example_data: list[str]):
    example_equations = [parse_equation(line) for line in example_data]
    assert is_valid_equation(example_equations[0]) is True
    assert is_valid_equation(example_equations[3]) is False

def test_exercise_one_example(example_data_file: Path):
    assert exercise_one(example_data_file) == 3749