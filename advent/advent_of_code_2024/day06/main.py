from typing import Generator, Iterator
from pathlib import Path

from advent.common.data_stream import stream_lines_from_file

DATA_DIR = Path(__file__).parent
DATA_00_PATH = DATA_DIR / "data_00.txt"
DATA_01_PATH = DATA_DIR / "data_01.txt"

def parse_lines_to_grid_entries(file_stream: Generator[str, None, None]) -> Iterator[tuple[int, int, str]]:
    for line_num, line in enumerate(file_stream):
        for char_num, character in enumerate(line):
            yield (char_num, line_num, character)

def update_direction(direction: tuple[int, int], reverse: bool = False) -> tuple[int, int]:
    """
    returns the updated direction when the guard reaches an obstacle.
    
    assumes the guard turns right, by default
    """
    directions: list[tuple[int, int]] = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1)
    ]
    ind_change: int = 1

    if reverse:
        ind_change = -1

    new_direction: tuple[int, int] = directions[(directions.index(direction) + ind_change) % 4]

    return new_direction

def calc_next_step(location: tuple[int, int], direction: tuple[int, int], map_dict: dict[tuple[int, int], str]) -> tuple[int, int] | None:
    """
    given the guards location and direction and the map of the complex,
    return his next step, taking into consideration obstacles.
    if the next step is not in the map, return None
    """
    loc: tuple[int, int] | None = (
        location[0] + direction[0],
        location[1] + direction[1]
    )

    if loc in map_dict:
        if map_dict[loc] == "#":
            new_direction: tuple[int, int] = update_direction(direction)
            loc = calc_next_step(location, new_direction, map_dict)
    else:
        loc = None

    return loc

def exercise_one(file_path: Path = DATA_01_PATH):
    line_stream = stream_lines_from_file(file_path)
    map_stream = parse_lines_to_grid_entries(line_stream)
    map_dict: dict[tuple[int, int], str] = {}

    for xcor, ycor, character in map_stream:
        map_dict[(xcor, ycor)] = character

    print(map_dict)

if __name__ == "__main__":
    print(f"exercise one: {exercise_one(DATA_00_PATH)}")