import pytest
from pathlib import Path

from advent.advent_of_code_2024.day09.main import (
    expand_diskmap,
    find_checksum,
    exercise_one
)

@pytest.fixture
def example_disk_map() -> str:
    return "2333133121414131402"

# TODO: how does this work with tmp_path?
@pytest.fixture
def example_data_file(tmp_path: Path, example_disk_map: str):
    fake_file = tmp_path / "day09_example_disk_map.txt"
    fake_file.write_text(example_disk_map)
    return fake_file

@pytest.fixture
def example_expanded_disk_map() -> str:
    return "00...111...2...333.44.5555.6666.777.888899"

@pytest.fixture
def example_compressed_disk_map() -> str:
    return "0099811188827773336446555566.............."

@pytest.fixture
def example_final_checksum() -> int:
    return 1928

def test_expand_diskmap(example_disk_map: str, example_expanded_disk_map: str):
    assert expand_diskmap(example_disk_map) == example_expanded_disk_map



def test_find_checksum(example_expanded_disk_map: str, example_final_checksum: int):
    assert find_checksum(example_expanded_disk_map) == example_final_checksum

def test_exercise_one_example(example_data_file: Path, example_final_checksum: int):
    assert exercise_one(example_data_file) == example_final_checksum
