import re

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

def exercise_one():
    pass

TEST_LINE = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"

if __name__ == "__main__":
    print("test:")
    print(line_to_funcs(TEST_LINE))
    print(2 * 2)