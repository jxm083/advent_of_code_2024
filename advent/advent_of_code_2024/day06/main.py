from typing import Generator, Iterator
from pathlib import Path

from advent.common.data_stream import stream_lines_from_file

DATA_DIR: Path = Path(__file__).parent
DATA_00_PATH: Path = DATA_DIR / "data_00_example_1.txt"
DATA_01_PATH: Path = DATA_DIR / "data_01.txt"

def parse_guard_direction(arrow: str) -> tuple[int, int] | None:
    direction: tuple[int, int] | None = (0, 0)

    match arrow:
        case ">":
            direction = (1, 0)
        case "v":
            direction = (0, 1)
        case "<":
            direction = (-1, 0)
        case "^":
            direction = (0, -1)
        case _:
            direction = None
    
    return direction

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

def calc_guard_path(location: tuple[int, int], direction: tuple[int, int], map_dict: dict[tuple[int, int], str]) -> list[tuple[int, int]]:
    guard_path: list[tuple[int, int]] = [location]
    next_location: tuple[int, int] | None = calc_next_step(location, direction, map_dict)

    while next_location is not None:
        current_location = next_location
        new_direction: tuple[int, int] = (
            current_location[0] - guard_path[-1][0],
            current_location[1] - guard_path[-1][1]
        )
        guard_path.append(current_location)
        next_location = calc_next_step(current_location, new_direction, map_dict)

    return guard_path

def exercise_one(file_path: Path = DATA_01_PATH) -> int:
    line_stream = stream_lines_from_file(file_path)
    map_stream = parse_lines_to_grid_entries(line_stream)
    map_dict: dict[tuple[int, int], str] = {}
    guard_path: list[tuple[int, int]] = []
    guard_pos_init: tuple[int, int] | None = None
    guard_direction_init: tuple[int, int] | None = None

    for xcor, ycor, character in map_stream:
        pos = (xcor, ycor)
        map_dict[pos] = character

        if len(guard_path) == 0:
            guard_direction_init = parse_guard_direction(character)
            if guard_direction_init is not None:
                guard_pos_init = pos

    if guard_direction_init is not None and guard_pos_init is not None:
        guard_path = calc_guard_path(
            location=guard_pos_init,
            direction=guard_direction_init,
            map_dict=map_dict
        )
    
    return len(guard_path)

if __name__ == "__main__":
    print(DATA_00_PATH)
    print(DATA_DIR)
    print(f"exercise one: {exercise_one(DATA_00_PATH)}")