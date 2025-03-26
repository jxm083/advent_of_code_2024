from typing import NamedTuple, TypeAlias, TypeVar, Callable, Iterator
from pathlib import Path

from advent.common.vectors import Vector
from advent.common.data_stream import stream_position_and_char, CharPosition


class MapPoint(NamedTuple):
    position: Vector
    height: int | None


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

    for position in potential_next_positions(trailhead_point.position):
        map_point = find_map_point(position, topo_map)
        if map_point is not None and map_point.height is not None and trailhead_point.height is not None:
            height_difference = map_point.height - trailhead_point.height
            if height_difference == 1:
                first_segments.append((trailhead_point, map_point))
    
    return first_segments

    


        


def get_next_segments(): ...


def get_height(): ...


def is_trailhead(): ...


def step_directions() -> Iterator[Vector]:
    directions = [Vector([1, 0]), Vector([0, -1]), Vector([-1, 0]), Vector([0, 1])]

    for vector in directions:
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
