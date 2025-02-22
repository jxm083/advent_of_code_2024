from pathlib import Path
from functools import partial

from advent.common.data_stream import stream_lines_from_file
from advent.advent_of_code_2024.day06.main import (
    parse_lines_to_grid_entries,
    update_direction,
    calc_next_step,
    parse_guard_direction,
    is_path_loop,
    exercise_one,
    exercise_two
)
import advent.advent_of_code_2024.day06.main as test_script
DATA_DIR: Path = Path(test_script.__file__).parent
DATA_PATH_00 = DATA_DIR / "data_00_example_1.txt"

def test_update_direction():
    assert update_direction((0, 1)) == (-1, 0)
    assert update_direction((0, 1), reverse=True) == (1, 0)
    assert update_direction((1, 0)) == (0, 1)
    assert update_direction((0, -1)) == (1, 0)
    assert update_direction((-1, 0)) == (0, -1)

first_test_entries: list[tuple[int, int, str]] = [
    (0, 0, "."),
    (1, 0, "."),
    (2, 0, "."),
    (3, 0, "."),
    (4, 0, "#"),
    (5, 0, "."),
    (6, 0, "."),
    (7, 0, "."),
    (8, 0, "."),
    (9, 0, "."),
    (0, 1, "."),
]

def test_parse_lines_to_grid_entries():
    file_stream = stream_lines_from_file(DATA_PATH_00)
    entry_stream = parse_lines_to_grid_entries(file_stream)
    for ind, (entry, test_entry) in enumerate(zip(entry_stream, first_test_entries)):
        if ind <= len(first_test_entries):
            assert entry == test_entry
        else:
            break

dummy_map_dict: dict[tuple[int, int], str] = {
    (0, 0): ".",
    (1, 0): "#",
    (2, 0): ".",
    (0, 1): ".",
    (1, 1): ".",
    (2, 1): "#",
    (0, 2): ".",
    (1, 2): "^",
    (2, 2): ".",
}

dummy_map_dict_loop: dict[tuple[int, int], str] = {
    (0, 0): ".",
    (1, 0): "#",
    (2, 0): ".",
    (3, 0): ".",
    (0, 1): ".",
    (1, 1): ".",
    (2, 1): ".",
    (3, 1): "#",
    (0, 2): "#",
    (1, 2): "^",
    (2, 2): ".",
    (3, 2): ".",
    (0, 3): ".",
    (1, 3): ".",
    (2, 3): "#",
    (3, 3): ".",
}

def test_calc_next_step_dummy():
    calc_next_step_dum = partial(calc_next_step, map_dict=dummy_map_dict)

    # go left
    assert calc_next_step_dum(
        location=(1, 1),
        direction=(-1, 0)
    ) == (0, 1)

    # go down
    assert calc_next_step_dum(
        location=(1, 1),
        direction=(0, 1)
    ) == (1, 2)

    # go right, encounter an obstacle
    assert calc_next_step_dum(
        location=(1, 1),
        direction=(1, 0)
    ) == (1, 2)

    # go up, encounter two obstacles
    assert calc_next_step_dum(
        location=(1, 1),
        direction=(0, -1)
    ) == (1, 2)

    # now try walking off the grid
    assert calc_next_step_dum(
        location=(2, 2),
        direction=(1, 0)
    ) is None

def test_parse_guard_direction():
    assert parse_guard_direction("v") == (0, 1)
    assert parse_guard_direction("<") == (-1, 0)
    assert parse_guard_direction("^") == (0, -1)
    assert parse_guard_direction(">") == (1, 0)

def test_is_path_loop():
    assert is_path_loop(dummy_map_dict_loop) == True
    assert is_path_loop(dummy_map_dict) == False

def test_exercise_one_example():
    assert exercise_one(DATA_PATH_00) == 41

def test_exercise_one_real():
    assert exercise_one() == 4374

def test_exercise_two_example():
    assert exercise_two(DATA_PATH_00) == 6

if __name__ == "__main__":
    print(
        calc_next_step(
            location=(1,1),
            direction=(0, -1),
            map_dict=dummy_map_dict
        )
    )