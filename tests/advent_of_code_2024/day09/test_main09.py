import pytest
from pathlib import Path
from itertools import starmap
from typing import Iterable

from advent.common.extended_itertools import flatten
from advent.advent_of_code_2024.day09.main import (
    BlockSizeAndID,
    MemoryBlock,
    translate_memory_string_to_file_id_stream,
    translate_file_id_to_str,
    translate_file_id_stream_to_memory_string,
    stream_diskmap,
    parse_block_pair,
    parse_block_pairs_to_indexed_memory_stream,
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
def example_expanded_memory_string() -> str:
    return "00...111...2...333.44.5555.6666.777.888899"


@pytest.fixture
def example_expanded_memory() -> Iterable[int | None]:
    memory = flatten(
        [
            2 * [0],
            3 * [None],
            3 * [1],
            3 * [None],
            1 * [2],
            3 * [None],
            3 * [3],
            1 * [None],
            2 * [4],
            1 * [None],
            4 * [5],
            1 * [None],
            4 * [6],
            1 * [None],
            3 * [7],
            1 * [None],
            4 * [8],
            2 * [9],
        ]
    )
    return memory


@pytest.fixture
def example_compressed_memory_string() -> str:
    return "0099811188827773336446555566.............."


@pytest.fixture
def example_compressed_memory() -> Iterable[int | None]:
    memory = flatten(
        [
            2 * [0],
            2 * [9],
            1 * [8],
            3 * [1],
            3 * [8],
            1 * [2],
            3 * [7],
            3 * [3],
            1 * [6],
            2 * [4],
            1 * [6],
            4 * [5],
            2 * [6],
            14 * [None],
        ]
    )
    return memory


@pytest.fixture
def example_final_checksum() -> int:
    return 1928


def test_translate_memory_string_to_file_id_stream_compressed(
    example_compressed_memory_string: str,
    example_compressed_memory: Iterable[int | None],
):
    reference_file_ids = list(example_compressed_memory)
    test_file_ids = list(
        translate_memory_string_to_file_id_stream(example_compressed_memory_string)
    )
    assert test_file_ids == reference_file_ids


def test_translate_file_id_to_str():
    assert translate_file_id_to_str(1) == "1"
    assert translate_file_id_to_str(None) == "."


def test_translate_file_id_stream_to_memory_string(
    example_expanded_memory: Iterable[int | None], example_expanded_memory_string: str
):
    reference_str = example_expanded_memory_string
    test_str = translate_file_id_stream_to_memory_string(example_expanded_memory)
    assert test_str == reference_str


@pytest.fixture
def simple_diskmap() -> str:
    return "12345"

@pytest.fixture
def simple_block_pair_stream() -> Iterable[BlockSizeAndID]:
    stream = starmap(BlockSizeAndID, [(1, 2, 0), (3, 4, 1), (5, 0, 2)])
    return stream

@pytest.fixture
def simple_expanded_indexed_memory_stream() -> Iterable[MemoryBlock]:
    stream = starmap(MemoryBlock, [
        (0, 0),
        (1, None),
        (2, None),
        (3, 1),
        (4, 1),
        (5, 1),
        (6, None),
        (7, None),
        (8, None),
        (9, None),
        (10, 2),
        (11, 2),
        (12, 2),
        (13, 2),
        (14, 2),
    ])
    return stream

@pytest.fixture
def simple_compressed_indexed_memory_stream() -> Iterable[MemoryBlock]:
    stream = starmap(MemoryBlock, [
        (0, 0),
        (1, 2),
        (2, 2),
        (3, 1),
        (4, 1),
        (5, 1),
        (6, 2),
        (7, 2),
        (8, 2),
        (9, None),
        (10, None),
        (11, None),
        (12, None),
        (13, None),
        (14, None),
    ])
    return stream



def test_stream_diskmap(simple_diskmap: str, simple_block_pair_stream: Iterable[BlockSizeAndID]):
    test = list(stream_diskmap(simple_diskmap))
    reference = list(simple_block_pair_stream)
    assert test == reference


def test_parse_block_pair():
    assert list(parse_block_pair(BlockSizeAndID(2, 3, 18))) == [
        18,
        18,
        None,
        None,
        None,
    ]

def test_parse_block_pairs_to_indexed_memory_stream(simple_block_pair_stream: Iterable[BlockSizeAndID], simple_expanded_indexed_memory_stream: Iterable[MemoryBlock]):
    reference = simple_expanded_indexed_memory_stream
    test = parse_block_pairs_to_indexed_memory_stream(
        simple_block_pair_stream
    )
    assert list(reference) == list(test)



def test_expand_diskmap(example_disk_map: str, example_expanded_disk_map: str):
    reference = [char for char in "0..111....22222"]
    expanded_diskmap = list(expand_diskmap("12345"))
    assert expanded_diskmap == reference

    reference_string = "00...111...2...333.44.5555.6666.777.888899"
    reference = [char for char in reference_string]
    expanded_diskmap = list(expand_diskmap(example_disk_map))
    assert expanded_diskmap == reference


def test_compress_expanded_diskmap(
    example_expanded_disk_map: str, example_compressed_disk_map: str
):
    assert (
        compress_expanded_diskmap(example_expanded_disk_map)
        == example_compressed_disk_map
    )


def test_find_checksum_from_compressed_diskmap(
    example_compressed_disk_map: str, example_final_checksum: int
):
    assert (
        find_checksum_from_compressed_diskmap(example_compressed_disk_map)
        == example_final_checksum
    )


def test_find_checksum(example_disk_map: str, example_final_checksum: int):
    assert find_checksum(example_disk_map) == example_final_checksum


def test_exercise_one_example(example_data_file: Path, example_final_checksum: int):
    assert exercise_one(example_data_file) == example_final_checksum


def test_exercise_one_real():
    assert exercise_one() > 90328963761
