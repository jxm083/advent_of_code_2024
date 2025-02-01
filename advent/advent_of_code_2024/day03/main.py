import re
from pathlib import Path

# A list of regular expressions describing all of the functions
FUNC_PATTERNS: list[str] = [
'mul\\([\\d]{1,3},[\\d]{1,3}\\)', # CHANGE to raw string
'do\\(\\)', # LOOK AT CAPTURE GROUPS
"don't\\(\\)"
]

def line_to_funcs(line: str, func_patterns: list[str] = FUNC_PATTERNS) -> list[str]:
    """
    Takes a line of corrupted code and returns
    a list of correct instructions. Defaults to the "mul" function.
    
    Assumes functions will not be nested and have form func(arg0, ..., argN)

    Args:
        line (str): a string of corrupt code
        func_patterns (list[str]): a list of valid function patterns

    Returns:
        list[str]: a list containing the strings of all valid functions
    """
    separator: str = "|"
    func_patterns_all: str = separator.join(func_patterns) 

    funcs: list[str] = []

    pattern = re.compile(func_patterns_all) 
    funcs = pattern.findall(line) 

    return funcs

def evaluate_mul_str(func_str: str) -> int: 
    """
    Takes a string expressing a function and evaluates the function.
    
    Assumes the function has two arguments that are ints.
    
    Args:
        func_str (str): a string expressing the function to be evaluated
        func (function?): the function to be evaluated
        
    Returns:
        int: the result of the evaluation
    """
    arg_pattern = re.compile('[\\d]{1,3}')

    args = [int(x) for x in arg_pattern.findall(func_str)] 

    return args[0] * args[1]

DATA_DIR = Path(__file__).parent

def exercise_one(file_name: str = "data01.txt", file_dir: Path = DATA_DIR):
    file_path = DATA_DIR / Path(file_name) 

    func_strs: list[str] = []

    with file_path.open() as file:

        for line in file.readlines():
            # Pull only mul(arg0, arg1) functions out of the line
            func_strs += line_to_funcs(line, func_patterns = [FUNC_PATTERNS[0]])
    
    evaluated_funcs: list[int] = [
        evaluate_mul_str(func_str) for func_str in func_strs
    ]

    return sum(evaluated_funcs)

def exercise_two(file_name: str = "data01.txt", file_dir: Path = DATA_DIR):
    file_path = DATA_DIR / Path(file_name)

    func_strs: list[str] = []

    with file_path.open() as file:

        for line in file.readlines():
            func_strs += line_to_funcs(line)

    last_logic_bit: int = 1
    total: int = 0

    for func_str in func_strs:
        if func_str == "do()":
            last_logic_bit = 1
        elif func_str == "don't()":
            last_logic_bit = 0
        else:
            total += last_logic_bit * evaluate_mul_str(func_str)

    return total


if __name__ == "__main__":
    print(f"Sum of products: {exercise_one()}")
    print(f"ibid w/ logic: {exercise_two()}")