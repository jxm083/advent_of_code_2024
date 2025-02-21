from pathlib import Path

from advent.common.data_stream import stream_lines_from_file
from advent.advent_of_code_2024.day06.main import (
    parse_lines_to_grid_entries,
    update_direction
)
import advent.advent_of_code_2024.day06.main as test_script
DATA_DIR: Path = Path(test_script.__file__).parent
DATA_PATH_00 = DATA_DIR / "data_00_example_1.txt"

def test_update_direction():
    assert update_direction((0, 1)) == (1, 0)
    assert update_direction((0, 1), reverse=True) == (-1, 0)
    assert update_direction((1, 0)) == (0, -1)
    assert update_direction((0, -1)) == (-1, 0)
    assert update_direction((-1, 0)) == (0, 1)

first_test_entries: list[tuple[int, int, str]] = [
    (0, 0, "."),
    (0, 1, "."),
    (0, 2, "."),
    (0, 3, "."),
    (0, 4, "#"),
    (0, 5, "."),
    (0, 6, "."),
    (0, 7, "."),
    (0, 8, "."),
    (0, 9, "."),
    (1, 0, "."),
]

def test_parse_lines_to_grid_entries():
    file_stream = stream_lines_from_file(DATA_PATH_00)
    entry_stream = parse_lines_to_grid_entries(file_stream)
    for ind, (entry, test_entry) in enumerate(zip(entry_stream, first_test_entries)):
        if ind <= len(first_test_entries):
            assert entry == test_entry
        else:
            break

def test_calc_next_step():
    pass