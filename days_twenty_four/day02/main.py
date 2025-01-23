from pathlib import Path

from days_twenty_four.common.import_data import import_data

DATA_DIR = Path(__file__).parents[0]

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
    for level in level_list[1:]:
        diff = previous_level - level
        if (
            abs(diff) <= max_diff and
            abs(diff) >= min_diff and
            diff * previous_diff > 0
        ):
            previous_level = level
            previous_diff = diff

        # If it is the first bad level with the dampner on, note it and continue
        elif bad_level_cnt == 0 and dampner:
            bad_level_cnt += 1
            print(f"Unsafe level: {level}")

        else:
            safe = False
            break

    return safe


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
        if is_safe(levels, dampner = True):
            safe_levels += 1

    return safe_levels

if __name__ == "__main__":
    print(f"Number of safe levels: {exercise_one()}") # 341
    print(f"Number of safe levels w/ dampner: {exercise_two("data00.csv")}") # 378