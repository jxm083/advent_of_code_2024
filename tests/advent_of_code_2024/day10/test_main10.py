from advent.common.vectors import Vector
from advent.common.data_stream import CharPosition
from advent.advent_of_code_2024.day10.main import (
    MapPoint,
    parse_to_map_point,
)

def test_parse_to_map_point():
    reference = MapPoint(Vector([0, 0]), 5)
    test = parse_to_map_point(CharPosition(Vector([0, 0]), "5"))
    assert test == reference

def test():
    assert Vector([0, 0]) == Vector([0, 0])