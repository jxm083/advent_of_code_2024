import pytest
from pathlib import Path
from re import search, findall

from advent.advent_of_code_2024.day09.main import (
    create_file_block,
    create_free_block,
    create_file_free_pair,
    parse_diskmap,
    expand_diskmap,
    compress_expanded_diskmap,
    find_checksum_from_compressed_diskmap,
    find_checksum,
    exercise_one,
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


def test_create_file_block():
    assert create_file_block(3, 1) == "111"


def test_create_free_block():
    assert create_free_block(5) == "....."


def test_create_file_free_pair():
    assert create_file_free_pair("3", "5", 1) == "111....."


def test_parse_diskmap():
    reference = [(0, "1", "2"), (1, "3", "4"), (2, "5", "0")]
    assert list(parse_diskmap("12345")) == reference


def test_expand_diskmap(example_disk_map: str, example_expanded_disk_map: str):
    reference = ["0..", "111....", "22222"]
    expanded_diskmap = expand_diskmap("12345")
    assert list(expanded_diskmap) == reference

    reference = ["00...", "111...", "2...", "333.", "44.", "5555.", "6666.", "777.", "8888", "99"]
    expanded_diskmap = expand_diskmap(example_disk_map)
    assert list(expanded_diskmap) == reference

def test_compress_expanded_diskmap(example_expanded_disk_map: str, example_compressed_disk_map: str):
    assert compress_expanded_diskmap(example_expanded_disk_map) == example_compressed_disk_map



def test_find_checksum_from_compressed_diskmap(example_compressed_disk_map: str, example_final_checksum: int):
    assert find_checksum_from_compressed_diskmap(example_compressed_disk_map) == example_final_checksum


def test_find_checksum(example_compressed_disk_map: str, example_final_checksum: int):
    assert find_checksum(example_compressed_disk_map) == example_final_checksum


def test_exercise_one_example(example_data_file: Path, example_final_checksum: int):
    assert exercise_one(example_data_file) == example_final_checksum
