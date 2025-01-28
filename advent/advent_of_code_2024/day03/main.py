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

    pattern = re.compile('mul\([\d]{1,3},[\d]{1,3}\)')
    funcs = pattern.findall(line)

    return funcs

def exercise_one():
    pass

TEST_LINE = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"

if __name__ == "__main__":
    print("test:")
    print(line_to_funcs(TEST_LINE))