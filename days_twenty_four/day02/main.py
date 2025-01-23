from pathlib import Path

from days_twenty_four.common.import_data import import_data

DATA_DIR = Path(__file__).parents[0]

def is_safe_diff(difference: int, previous_difference: int) -> bool:
    """
    Looks at the difference between two levels and the difference between
    the previous two levels and indicates whether the differences are safe,
    as defined by
    (a) the current and previous differences are of the same sign
    (b) the current difference is at least one and at most three
    """
    max_diff = 3
    min_diff = 1

    return (abs(difference) >= min_diff and 
            abs(difference) <= max_diff and
            difference * previous_difference > 0)

def is_safe(level_list: list[int], dampner: bool = False) -> bool:
    """
    Takes in a list of levels and deems it safe if
    (a) the levels are all increasing or all decreasing, and
    (b) any two adjacent levels differ by at least one and at most three

    level_list must be at least two elements.

    Args:
        level_list (list[int]): the list of levels
        dampner (bool): indicates if the dampner is engaged

    Returns:
        bool: whether the levels are safe or not
    """
    # Check that the level_list has at least two elements.
    assert len(level_list) > 1

    max_diff = 3
    min_diff = 1

    previous_level = level_list[0]
    previous_diff = level_list[0] - level_list[1]

    safe = True
    bad_level_cnt = 0

    # Starting with the second level, find the differences
    # between adjacent levels
    for num, level in enumerate(level_list[1:]):
        diff = previous_level - level
        if is_safe_diff(diff, previous_diff):
            previous_level = level
            previous_diff = diff

        elif dampner and bad_level_cnt == 0:
            bad_level_cnt += 1

            if num == 1 or num == 0:
                l = level_list
                if is_safe_diff(l[2] - l[3], l[1] - l[2]):
                    previous_level = l[1]
                    previous_diff = l[1] - l[2]

                elif is_safe_diff(l[2] - l[3], l[0] - l[2]):
                    previous_level = l[0]
                    previous_diff = l[0] - l[2]

                else:
                    AssertionError("Unforseen problem")

        else:
            safe = False
            break

    return safe

def is_safe_w_dampner(level_list: list[int]) -> bool:
    """
    """
    


def exercise_one(file_name: str | None = "data01.csv", file_dir: Path | None = DATA_DIR):
    data = import_data(file_name, file_dir)

    safe_levels = 0

    for levels in data:
        if is_safe(levels):
            safe_levels += 1
    
    return safe_levels

def exercise_two(file_name: str | None = "data01.csv", file_dir: Path | None = DATA_DIR):
    data = import_data(file_name, file_dir)

    safe_levels = 0

    for levels in data:
        if is_safe(levels):
            safe_levels += 1
        else:
            safe_w_dampner = False
            for n, _ in enumerate(levels):
                levels_temp = levels
                levels_temp.pop(n)
                if is_safe(levels_temp) and not safe_w_dampner:
                    safe_levels += 1
                    safe_w_dampner = True

    return safe_levels

edge_cases = [
    [3,2,3,4,5],
    [1,5,6,7,8],
    [1,2,3,4,8],
    [1,2,3,4,3],
    [1,2,3,4,5]
]

if __name__ == "__main__":
    for id, case, in enumerate(edge_cases):
        print(f"{id} is safe: {is_safe(case, dampner=True)}")
    
    print(f"Number of safe levels: {exercise_one()}") # 341
    print(f"Number of safe levels w/ dampner: {exercise_two()}") # 507