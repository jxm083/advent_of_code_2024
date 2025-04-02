from typing import NamedTuple, TypeAlias, Callable, Iterator
from pathlib import Path
from functools import partial
from concurrent.futures import ProcessPoolExecutor

from advent.common.vectors import Vector
from advent.common.data_stream import stream_position_and_char, CharPosition


class MapPoint(NamedTuple):
    position: Vector
    height: int | None


class Segment(NamedTuple):
    start: MapPoint
    end: MapPoint


Map: TypeAlias = list[MapPoint]

DATA_DIR = Path(__file__).parent
EXAMPLE_DATA_PATH = DATA_DIR / "example_data.txt"
DATA_PATH = DATA_DIR / "data.txt"


## problem domain functions
def exercise_one(map_file_path: Path = DATA_PATH) -> int:
    topo_map = get_map(map_file_path)
    return get_map_metric(topo_map, get_trailhead_score)


def exercise_two(map_file_path: Path = DATA_PATH) -> int:
    topo_map = get_map(map_file_path)
    return get_map_metric(topo_map, get_trailhead_rating)


def get_map_metric(
    topo_map: Map, get_trail_metric: Callable[[Map, MapPoint], int]
) -> int:
    trailheads = filter(is_trailhead, topo_map)
    get_trail_metric_partial = partial(get_trail_metric, topo_map)

    with ProcessPoolExecutor() as executor:
        trail_metrics = executor.map(get_trail_metric_partial, trailheads)

    return sum(trail_metrics)


def get_trailhead_score(topo_map: Map, trailhead: MapPoint) -> int:
    unique_trail_ends = get_unique_trail_ends(trailhead, topo_map)
    return len(unique_trail_ends)


def get_trailhead_rating(topo_map: Map, trailhead: MapPoint) -> int:
    trail_ends = get_trail_ends(trailhead, topo_map)
    return len(trail_ends)


## intermediate functions
def get_map(map_file_path: Path) -> Map:
    position_char_stream = stream_position_and_char(map_file_path)
    return list(map(parse_to_map_point, position_char_stream))


def parse_to_map_point(position_char: CharPosition) -> MapPoint:
    try:
        height = int(position_char.char)
    except ValueError:
        height = None

    position = position_char.position

    return MapPoint(position, height)


def find_map_point(position: Vector, topo_map: Map) -> MapPoint | None:
    map_positions = [point.position for point in topo_map]
    map_point: MapPoint | None = None
    try:
        index = map_positions.index(position)
        map_point = topo_map[index]  # type: ignore
    except ValueError:
        map_point = None

    return map_point


# TODO: reframe in the positive: forward_step, heights_set, proper_height_change
def is_valid_next_step(
    current_segment: Segment, point: MapPoint
) -> bool:
    retraced_step = point.position == current_segment.start.position
    heights_set = isinstance(point.height, int) and isinstance(current_segment[1].height, int)

    if heights_set:
        proper_height_change = (point.height - current_segment.end.height) == 1 # type: ignore
    else:
        proper_height_change = False

    return proper_height_change and not retraced_step


# TODO: consolidate with get_next_segments
def get_first_segments(
    trailhead_point: MapPoint, topo_map: Map
) -> list[tuple[MapPoint, MapPoint]]:
    first_segments: list[tuple[MapPoint, MapPoint]] = []
    off_map_position = Vector([-1, -1])
    # In order to use is_valid_next_step, which takes into
    # consideration the previous step, we need to create
    # a segment whose previous step is certainly not in the map.
    zeroth_segment = (MapPoint(off_map_position, None), trailhead_point)

    for position in potential_next_positions(trailhead_point.position):
        map_point = find_map_point(position, topo_map)
        if map_point is not None and is_valid_next_step(zeroth_segment, map_point):
            first_segments.append((trailhead_point, map_point))

    return first_segments


def get_next_segments(
    current_segment: tuple[MapPoint, MapPoint], topo_map: Map
) -> list[Segment]:
    next_segments: list[Segment] = []
    for position in potential_next_positions(current_segment[1].position):
        map_point = find_map_point(position, topo_map)
        if map_point is not None and is_valid_next_step(current_segment, map_point):
            next_segments.append(Segment(current_segment[1], map_point))

    return next_segments


def is_final_segment(segment: Segment) -> bool:
    return segment.end.height == 9


def get_trail_ends(trailhead: MapPoint, topo_map: Map) -> list[MapPoint]:
    current_segments = get_first_segments(trailhead, topo_map)
    trail_ends: list[MapPoint] = []

    while len(current_segments) != 0:
        next_segments: list[Segment] = []
        for segment in current_segments:
            next_segments += get_next_segments(segment, topo_map)

        trail_ends += [
            segment.end for segment in filter(is_final_segment, next_segments)
        ]

        current_segments = next_segments

    return trail_ends


def get_unique_trail_ends(trailhead: MapPoint, topo_map: Map) -> list[MapPoint]:
    trail_ends = get_trail_ends(trailhead, topo_map)
    return list(set(trail_ends))


def is_trailhead(map_point: MapPoint) -> bool:
    return map_point.height == 0


DIRECTIONS = (Vector([1, 0]), Vector([0, -1]), Vector([-1, 0]), Vector([0, 1]))


def step_directions() -> Iterator[Vector]:
    for vector in DIRECTIONS:
        yield vector


def potential_next_positions(position: Vector) -> Iterator[Vector]:
    for step in step_directions():
        yield position + step


if __name__ == "__main__":
    print(f"exercise one: {exercise_one()}")
    print(f"exercise two: {exercise_two()}")
