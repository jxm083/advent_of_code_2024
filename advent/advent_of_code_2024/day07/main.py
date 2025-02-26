from pathlib import Path
from typing import TypeAlias, Callable, Iterator
from re import findall
from operator import add, mul
from itertools import product
from functools import partial
from concurrent.futures import ProcessPoolExecutor

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
# TODO: confirm the difference between Iterable and Iterator
def generate_function_combo(number_of_terms: int, function_list: FunctionList = LIST_OF_FUNCTIONS) -> Iterator[FunctionList]:
    combinations = product(function_list, repeat=number_of_terms - 1)
    for combo in combinations:
        yield combo

def evaluate_function_combos(terms: tuple[int,...], function_list: FunctionList = LIST_OF_FUNCTIONS) -> Iterator[int]:
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

    function_evaluations: Iterator[int] = evaluate_function_combos(terms, function_list=function_list)

    for eval in function_evaluations:
        if eval == answer:
            valid_equation = True
            break

    return valid_equation

def concatenate_ints(int0: int, int1: int) -> int:
    """
    Concatenates two integers, e.g. 
    concatenate_ints(142, 16) -> 14216
    
    ASSUMES the second int, int1, is no more than three digits long.
    
    Args:
        int0 (int): first integer
        int1 (int): second integer
        
    Returns:
        int: concatenation of int0 and int1
    """
    if int1 == 0:
        return int0 * 10
    elif int1 <= 10:
        return int0 * 10 + int1
    elif int1 <= 100:
        return int0 * 100 + int1
    elif int1 <= 1000:
        return int0 * 1000 + int1
    else:
        raise ValueError("int1 has more than three digits")

def equation_bool_parser(equation: Equation, equation_filter: Callable[[Equation], bool]) -> int:
    output: int = 0
    if equation_filter(equation):
        output = equation[0]
    return output
    

def calibration_check(
    data_path: Path = DATA_01,
    function_list: FunctionList = LIST_OF_FUNCTIONS
    ) -> int: # TODO: make sure ruff is working

    data_stream = stream_lines_from_file(data_path)

    equation_filter: Callable[[Equation], bool] = partial(
        is_valid_equation,
        function_list = function_list
    )

    equation_bool_parser_temp: Callable[[Equation], int] = partial(
        equation_bool_parser,
        equation_filter=equation_filter
    )

    with ProcessPoolExecutor() as executor:
        valid_equations = executor.map(
            equation_bool_parser_temp,
            map(parse_equation, data_stream)
        )

    return sum(num for num in valid_equations)

def exercise_one(data_path: Path = DATA_01) -> int:
    return calibration_check(
        data_path=data_path
    )

def exercise_two(data_path: Path = DATA_01) -> int:
    function_list = *LIST_OF_FUNCTIONS, concatenate_ints
    return calibration_check(
        data_path=data_path,
        function_list=function_list
    )

if __name__ == "__main__":
    print(f"exercise one: {exercise_one()}")
    import time
    start = time.time()
    print(f"exercise two: {exercise_two()}")
    end = time.time()
    print(f"exercise two duration: {end - start} s")