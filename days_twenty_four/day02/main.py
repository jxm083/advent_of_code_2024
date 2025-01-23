from pathlib import Path

from days_twenty_four.common.import_data import import_data

DATA_DIR = Path(__file__).parents[0]

def is_safe(level_list: list[int]):
    """
    Takes in a list of levels and deems it safe if
    (a) the levels are all increasing or all decreasing, and
    (b) any two adjacent levels differ by at least one and at most three

    Assumes level_list has at least two elements.

    Args:
        level_list (list[int]) the list of levels

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

        else:
            safe = False
            break

    return safe


def exercise_one():
    data = import_data("data00.csv", DATA_DIR)

    safe_levels = 0

    for levels in data:
        if is_safe(levels):
            safe_levels += 1
    
    return safe_levels

if __name__ == "__main__":
    print(f"Number of safe levels: {exercise_one()}")