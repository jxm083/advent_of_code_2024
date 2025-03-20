from typing import NamedTuple, TypeAlias, Iterable
from pathlib import Path

from advent.common.vectors import Vector
from advent.common.data_stream import stream_position_and_char, CharPosition

class MapPoint(NamedTuple):
    position: Vector
    height: int | None

Map: TypeAlias = Iterable[MapPoint]



## problem domain functions
def exercise_one(): ...

def exercise_two(): ...

def get_trailhead_score(): ...
# "number of 9-height positions reachable from that trailhead via a hiking trail"

## intermediate functions
def get_map(map_file_path: Path) -> Map:
    position_char_stream = stream_position_and_char(map_file_path)
    return map(parse_to_map_point, position_char_stream)

def parse_to_map_point(position_char: CharPosition) -> MapPoint:
    try:
        height = int(position_char.char) 
    except ValueError:
        height = None

    position = position_char.position

    return MapPoint(position, height)
# map is an iterable of position-height pairs

def get_next_segments(): ...

def get_height(): ...

def is_trailhead(): ...

## solution domain functions

if __name__ == "__main__":
    pass