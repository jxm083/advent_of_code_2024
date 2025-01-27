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

    # All function calls will start with "func(", so append "(" to the func names
    # note that the open parenthesis needs to be escaped to be used by re
    func_starts: list[str] = [name + "\(" for name in func_names] # type: ignore
    print(func_starts)

    print([m.start() for m in re.finditer(func_starts[0], line)]) # type: ignore

    return funcs

def exercise_one():
    pass

TEST_LINE = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"

if __name__ == "__main__":
    print("test:")
    line_to_funcs(TEST_LINE)