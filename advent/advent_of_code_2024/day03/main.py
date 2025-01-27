def line_to_funcs(line: str, func_names: list[str] | None = ["mul"]) -> list[str]:
    """
    Takes a line of corrupted code and returns
    a list of correct instructions. Defaults to the "mul" function.
    
    Assumes functions will not be nested.

    Args:
        line (str): a string of corrupt code
        func_names (list[str]): a list of valid function names, defaults to ["mul"]

    Returns:
        list[str]: a list containing the strings of all valid functions
    """
    funcs: list[str] = []

    return funcs

def exercise_one():
    pass