from typing import NamedTuple, TypeAlias, TypeVar, Callable, Iterator
from pathlib import Path

from advent.common.vectors import Vector
from advent.common.data_stream import stream_position_and_char, CharPosition


class MapPoint(NamedTuple):
    position: Vector
    height: int | None

class Segment(NamedTuple):
    start: MapPoint
    end: MapPoint

Map: TypeAlias = list[MapPoint]


## problem domain functions
def exercise_one(): ...


def exercise_two(): ...


def get_trailhead_score(): ...


# "number of 9-height positions reachable from that trailhead via a hiking trail"


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


def is_valid_next_step(
    current_segment: tuple[MapPoint, MapPoint], point: MapPoint
) -> bool:
    retraced_step = point.position == current_segment[0].position
    heights_not_set = point.height is None or current_segment[1].height is None

    if point.height is not None and current_segment[1].height is not None:
        wrong_height_change = (point.height - current_segment[1].height) != 1
    else:
        wrong_height_change = True

    return not (retraced_step or heights_not_set or wrong_height_change)


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

def get_trail_ends(trailhead: MapPoint, topo_map: Map) -> list[Segment]:
    current_segments = get_first_segments(trailhead, topo_map)
    trail_ends: list[Segment] = []

    while len(current_segments) != 0:
        next_segments: list[Segment] = []
        for segment in current_segments:
            next_segments += get_next_segments(segment, topo_map)

        trail_ends += list(filter(is_final_segment, next_segments))

        current_segments = next_segments

    return trail_ends

        



    

def get_height(): ...


def is_trailhead(): ...


DIRECTIONS = [Vector([1, 0]), Vector([0, -1]), Vector([-1, 0]), Vector([0, 1])]
def step_directions() -> Iterator[Vector]:
    for vector in DIRECTIONS:
        yield vector


def potential_next_positions(position: Vector) -> Iterator[Vector]:
    for step in step_directions():
        yield position + step


## solution domain functions

T = TypeVar("T")


def make_map_boundary_filter(topo_map: Map) -> Callable[[Vector], bool]:
    map_list = list(topo_map)
    max_line = max(point.position[0] for point in map_list)
    max_char = max(point.position[1] for point in map_list)

    def map_boundary_filter(position: Vector) -> bool:
        in_bounds = False
        if 0 <= position[0] <= max_line and 0 <= position[1] <= max_char:
            in_bounds = True
        return in_bounds

    return map_boundary_filter


if __name__ == "__main__":
    pass
