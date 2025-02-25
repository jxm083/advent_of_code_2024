from dataclasses import dataclass
from typing import Generator, Iterator
from pathlib import Path
from copy import copy

from advent.common.data_stream import stream_lines_from_file

DATA_DIR: Path = Path(__file__).parent
DATA_00_PATH: Path = DATA_DIR / "data_00_example_1.txt"
DATA_01_PATH: Path = DATA_DIR / "data_01.txt"

type Map2d = list[list[str]]

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

DIRECTIONS: list[tuple[int, int]] = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]

@dataclass(slots=True)
class DirNode:
    name: str
    vector: tuple[int, int]
    turn: "DirNode"

def make_dir_chain() -> DirNode:
    up = DirNode("UP", (-1, 0), None) # type: ignore
    left = DirNode("LEFT", (0, -1), up)
    down = DirNode("DOWN", (1, 0), left)
    right = DirNode("RIGHT", (0, 1), down)
    up.turn = right

    return up

def update_direction(direction: tuple[int, int]) -> tuple[int, int]:
    """
    returns the updated direction when the guard reaches an obstacle.
    
    assumes the guard turns right, by default
    """
    new_direction: tuple[int, int] = DIRECTIONS[(DIRECTIONS.index(direction) + 1) % 4]

    return new_direction

def calc_next_step(location: tuple[int, int], direction: tuple[int, int], map2d: Map2d) -> tuple[int, int] | None:
    """
    given the guards location and direction and the map of the complex,
    return his next step, taking into consideration obstacles.
    if the next step is not in the map, return None
    """
    can_move: bool = False

    new_direction = direction
    loc = None

    while can_move is False:
        loc = (
            location[0] + new_direction[0],
            location[1] + new_direction[1]
        )
        try:
            symbol = map2d[loc[1]][loc[0]]
            if symbol == "#":
                new_direction = update_direction(new_direction)
            else:
                can_move = True
        except IndexError:
                can_move = True
                loc = None

    return loc

def calc_guard_path(location: tuple[int, int], direction: tuple[int, int], map2d: Map2d) -> list[tuple[int, int]]:
    trajectory_stream = stream_guard_trajectory(
        guard_location=location,
        guard_direction=direction,
        map2d=map2d
    )

    trajectory: list[tuple[tuple[int, int], tuple[int, int]]] = []

    for update in trajectory_stream:
        # This condition catches if the gaurd is in a loop
        # since he will hit the same location moving
        # in the same directions
        if update in trajectory:
            break
        else:
            trajectory.append(update)

    return [loc for loc, _ in trajectory]
    
def compile_initial_map(file_path: Path) -> tuple[Map2d, tuple[int, int] | None, tuple[int, int] | None]:
    line_stream: Generator[str, None, None] = stream_lines_from_file(file_path)
    map_stream = parse_lines_to_grid_entries(line_stream)

    map_flat = [datum for datum in map_stream]
    max_x_ind = map_flat[-1][0]
    max_y_ind = map_flat[-1][1]
    map_2d: Map2d = [[""] * (max_x_ind + 1) for _ in range((max_y_ind + 1))]
    guard_position: tuple[int, int] | None = None
    guard_direction: tuple[int, int] | None = None

    for xcor, ycor, character in map_flat:
        pos = (xcor, ycor)
        map_2d[ycor][xcor]= character

        if guard_direction is None:
            guard_direction = parse_guard_direction(character)
            if guard_direction is not None:
                guard_position = pos

    return map_2d, guard_position, guard_direction

def stream_guard_trajectory(
        guard_location: tuple[int, int] | None,
        guard_direction: tuple[int, int] | None,
        map2d: Map2d
) -> Iterator[tuple[tuple[int, int] | None, tuple[int, int] | None]]:
    next_location: tuple[int, int] | None = guard_location
    next_direction: tuple[int, int] | None = guard_direction

    while next_location is not None:
        loc = next_location
        dir = next_direction

        next_location = calc_next_step(
            location=next_location,
            direction=next_direction,
            map2d=map2d
        )

        if next_location is not None:
            next_direction = (
                next_location[0] - loc[0],
                next_location[1] - loc[1]
            )

        yield loc, dir
        
def is_path_loop(
        location: tuple[int, int], 
        direction: tuple[int, int], 
        map2d: Map2d
) -> bool: # TODO: best convention for formatting this def'n?
    path_loop: bool = False
    trajectory_stream = stream_guard_trajectory(
        guard_location=location,
        guard_direction=direction,
        map2d=map2d
    )

    trajectory: list[tuple[tuple[int, int] | None, tuple[int, int] | None]] = []

    for update in trajectory_stream:
        if update in trajectory:
            path_loop = True
            break
        else:
            trajectory.append(update)
    
    return path_loop

def collect_loop_obstacle_positions(
        guard_position: tuple[int, int] | None,
        guard_direction: tuple[int, int] | None,
        map2d: Map2d
) -> set[tuple[int, int]]:
    grd_trajectory_stream = stream_guard_trajectory(
        guard_location=guard_position,
        guard_direction=guard_direction,
        map2d=map2d
    )
    
    grd_trajectory: list[tuple[tuple[int, int] | None, tuple[int, int] | None]] = []

    for update in grd_trajectory_stream:
        if update in grd_trajectory:
            break
        else:
            grd_trajectory.append(update)

    grd_positions: list[tuple[int, int] | None] = [
        pos for pos, _ in grd_trajectory if pos != guard_position
    ]

    possible_obstacle_positions: list[tuple[int, int] | None] = list(set(grd_positions))
    loop_obstacle_positions: list[tuple[int, int]] = list()

    for num, obs_pos in enumerate(possible_obstacle_positions):
        new_map: Map2d = add_obstacle_to_map(
            initial_map=map2d,
            obstacle_position=obs_pos
        )

        ### ADDING NUM LIMIT TO LIMIT RUN TIME
        ### REMOVE IF FULL SOLUTION IS DESIRED
        if num > 250:
            break

        if is_path_loop(guard_position, guard_direction, new_map):
            loop_obstacle_positions.append(obs_pos)
            #print(f"{num + 1} / {len(possible_obstacle_positions)}, {len(loop_obstacle_positions)} found: {obs_pos}")

    return set(loop_obstacle_positions)

def add_obstacle_to_map(
        initial_map: Map2d,
        obstacle_position: tuple[int, int] | None
) -> Map2d:
    if obstacle_position is not None:
        new_map: Map2d = []
        temp_line: list[str] = []

        for line_num, line in enumerate(initial_map):
            if line_num == obstacle_position[1]:
                temp_line = copy(line)
                temp_line[obstacle_position[0]] = "#"
            else:
                temp_line = line

            new_map.append(temp_line)
    else:
        new_map = initial_map

    return new_map

def exercise_one(file_path: Path = DATA_01_PATH) -> int:
    map2d, guard_pos_init, guard_direction_init = compile_initial_map(file_path=file_path)

    guard_path: list[tuple[int, int]] = []

    if guard_direction_init is not None and guard_pos_init is not None:
        guard_path = calc_guard_path(
            location=guard_pos_init,
            direction=guard_direction_init,
            map2d=map2d
        )
    # return the length of the set to remove any duplicates from the path
    return len(set(guard_path))

def exercise_two(file_path: Path = DATA_01_PATH) -> int:
    map2d, guard_pos_init, guard_direction_init = compile_initial_map(
        file_path=file_path
    )

    if guard_pos_init is not None and guard_direction_init is not None:
        obstacle_positions: set[tuple[int, int]] = collect_loop_obstacle_positions(
            guard_position=guard_pos_init,
            guard_direction=guard_direction_init,
            map2d=map2d
    )
    else:
        obstacle_positions = set([])

    return len(obstacle_positions)

if __name__ == "__main__":
    #print(f"exercise one: {exercise_one()}")
    import time
    start = time.time()
    print(f"exercise two: {exercise_two()}")
    end = time.time()
    print(f"{end - start}")