import pytest
from pathlib import Path
from typing import Iterator
from itertools import starmap

from advent.common.vectors import Vector
from advent.common.data_stream import CharPosition
from advent.advent_of_code_2024.day10.main import (
    Map,
    MapPoint,
    parse_to_map_point,
    get_map,
    make_map_boundary_filter,
    step_directions,
    potential_next_positions,
    get_first_segments
)

@pytest.fixture
def simple_map_file() -> str:
    return """012
543
678
909
"""

@pytest.fixture
def simple_file_vectors() -> Iterator[Vector]:
    return map(Vector,
               [
                   [0, 0], [0, 1], [0, 2],
                   [1, 0], [1, 1], [1, 2],
                   [2, 0], [2, 1], [2, 2],
                   [3, 0], [3, 1], [3, 2]
               ])

@pytest.fixture
def simple_file_heights() -> list[int]:
    return [
        0, 1, 2,
        5, 4, 3,
        6, 7, 8,
        9, 0, 9
    ]

@pytest.fixture
def simple_map(simple_file_vectors: Iterator[Vector], simple_file_heights: list[int]) -> Map:
    return list(starmap(MapPoint, zip(simple_file_vectors, simple_file_heights)))

@pytest.fixture
def simple_file_path(tmp_path: Path, simple_map_file: str):
    path = tmp_path / "day10_simple_map.txt"
    path.write_text(simple_map_file)
    return path

def test_parse_to_map_point():
    reference = MapPoint(Vector([0, 0]), 5)
    test = parse_to_map_point(CharPosition(Vector([0, 0]), "5"))
    assert test == reference

def test_get_map(simple_file_path: Path, simple_map: Map):
    test = get_map(simple_file_path)
    reference = simple_map
    assert list(test) == list(reference)

def test_make_map_boundary_filter(simple_map: Map):
    boundary_filter = make_map_boundary_filter(simple_map)
    assert boundary_filter(Vector([0, 0])) is True
    assert boundary_filter(Vector([-1, 0])) is False
    assert boundary_filter(Vector([100, 100])) is False

def test_step_directions():
    test = step_directions()
    reference = [
        Vector([1, 0]),
        Vector([0, -1]),
        Vector([-1, 0]),
        Vector([0, 1])
    ]

    assert list(test) == reference

def test_potential_next_positions():
    position = Vector([0, 0])
    test = potential_next_positions(position)
    reference = [
        Vector([1, 0]),
        Vector([0, -1]),
        Vector([-1, 0]),
        Vector([0, 1])
    ]

    assert list(test) == list(reference)

def test_get_first_segments(simple_map: Map):
    trailhead_point = MapPoint(Vector([0, 0]), 0)
    next_step = MapPoint(Vector([0, 1]), 1)
    test = get_first_segments(trailhead_point, simple_map)
    reference = [(
        trailhead_point,
        next_step
    )]

    assert test == reference