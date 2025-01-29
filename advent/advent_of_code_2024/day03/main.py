import re
from pathlib import Path

from advent.common.import_data import import_data

def line_to_funcs(line: str, func_names: list[str] | None = ["mul"]) -> list[str]:
    """
    Takes a line of corrupted code and returns
    a list of correct instructions. Defaults to the "mul" function.
    
    Assumes functions will not be nested and have form func(arg0, ..., argN)

    Args:
        line (str): a string of corrupt code
        func_names (list[str]): a list of valid function names, defaults to ["mul"]

    Returns:
        list[str]: a list containing the strings of all valid functions
    """
    funcs: list[str] = []

    pattern = re.compile('mul\([\d]{1,3},[\d]{1,3}\)') # type: ignore
    funcs = pattern.findall(line)

    return funcs

def evaluate_func_str(func_str: str, func = int.__mul__) -> int:
    """
    Takes a string expressing a function and evaluates the function.
    
    Assumes the function has two arguments that are ints.
    
    Args:
        func_str (str): a string expressing the function to be evaluated
        func (function?): the function to be evaluated
        
    Returns:
        int: the result of the evaluation
    """
    arg_pattern = re.compile('[\d]{1,3}') # type: ignore

    args = [int(x) for x in arg_pattern.findall(func_str)] # type: ignore

    return func(args[0], args[1])

DATA_DIR = Path(__file__).parent

def exercise_one(file_name: str | None = "data01.txt", file_dir: Path | None = DATA_DIR):
    file_path = DATA_DIR / Path(file_name)

    func_strs: list[str] = []

    with file_path.open() as file:

        for line in file.readlines():
            func_strs += line_to_funcs(line)
    
    evaluated_funcs: list[int] = [
        evaluate_func_str(func_str) for func_str in func_strs
    ]

    return sum(evaluated_funcs)


if __name__ == "__main__":
    print(f"Sum of products: {exercise_one("data00.txt")}")