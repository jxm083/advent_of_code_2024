from pathlib import Path
from typing import TypeAlias, Callable, Iterable
from re import findall
from operator import add, mul
from itertools import product
from functools import partial

from advent.common.data_stream import stream_lines_from_file

DATA_DIR = Path(__file__).parent
EXAMPLE_DATA = DATA_DIR / "data00.txt"
DATA_01 = DATA_DIR / "data01.txt"

Equation: TypeAlias = tuple[int, tuple[int,...]]
def parse_equation(line: str) -> Equation: # TODO: fragile if file has empty lines at the end
    numbers = [int(num) for num in findall(r"\d+", line)] # TODO: why isn't findall returning a list?
    return (numbers[0], tuple(numbers[1:]))

FunctionList: TypeAlias = tuple[Callable[[int, int], int],...]
LIST_OF_FUNCTIONS: FunctionList = (add, mul)
# TODO: for part two had to add function_list variable everywhere---better design?
def generate_function_combo(number_of_terms: int, function_list: FunctionList = LIST_OF_FUNCTIONS) -> Iterable[FunctionList]:
    combinations = product(function_list, repeat=number_of_terms - 1)
    for combo in combinations:
        yield combo

def evaluate_function_combos(terms: tuple[int,...], function_list: FunctionList = LIST_OF_FUNCTIONS) -> Iterable[int]:
    function_combos = generate_function_combo(len(terms), function_list=function_list)

    for combo in function_combos:
        total = terms[0]
        for ind, function in enumerate(combo):
            total = function(total, terms[ind + 1])

        yield total

def is_valid_equation(equation: Equation, function_list: FunctionList = LIST_OF_FUNCTIONS) -> bool:
    answer = equation[0]
    terms = equation[1]
    valid_equation = False

    function_evaluations: Iterable[int] = evaluate_function_combos(terms, function_list=function_list)

    for eval in function_evaluations:
        if eval == answer:
            valid_equation = True

    return valid_equation

def concatenate_ints(int0: int, int1: int) -> int:
    return int(str(int0) + str(int1))

def exercise_one(data_path: Path = DATA_01) -> int:
    data_stream = stream_lines_from_file(data_path)

    valid_equations = filter(
        is_valid_equation,
        map(
            parse_equation,
            data_stream
        )
    )

    return sum(answer for answer, _ in valid_equations)

def exercise_two(data_path: Path = DATA_01) -> int:
    data_stream = stream_lines_from_file(data_path)

    function_list = *LIST_OF_FUNCTIONS, concatenate_ints
    is_valid_equation_concat: Callable[[Equation], bool] = partial(
        is_valid_equation,
        function_list = function_list
    )

    valid_equations = filter(
        is_valid_equation_concat,
        map(
            parse_equation,
            data_stream
        )
    )

    return sum(answer for answer, _ in valid_equations)

if __name__ == "__main__":
    print(f"exercise one: {exercise_one()}")
    print(f"exercise two: {exercise_two()}")