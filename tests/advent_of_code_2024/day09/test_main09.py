import pytest
from pathlib import Path
from itertools import starmap
from typing import Iterable

from advent.common.extended_itertools import flatten
from advent.advent_of_code_2024.day09.main import (
    BlockSizeAndID,
    IndexedMemoryUnit,
    MemoryBlock,
    translate_memory_string_to_file_id_stream,
    translate_file_id_to_str,
    translate_file_id_stream_to_memory_string,
    stream_block_pairs,
    stream_blocks,
    parse_block_pair,
    parse_block_pair_to_blocks,
    parse_block_pairs_to_memory_stream,
    parse_memory_stream_to_blocks,
    compress_memory_stream,
    fp_compress_memory,
    find_checksum_from_memory_stream,
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
def example_fp_compressed_memory_string() -> str:
    return  "00992111777.44.333....5555.6666.....8888.."

@pytest.fixture
def example_fp_compressed_memory(example_fp_compressed_memory_string: str) -> Iterable[int | None]:
    memory = translate_memory_string_to_file_id_stream(
        example_fp_compressed_memory_string
    )
    return memory

@pytest.fixture
def example_fp_final_checksum() -> int:
    return 2858

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
def simple_expanded_indexed_memory_stream() -> Iterable[IndexedMemoryUnit]:
    stream = starmap(IndexedMemoryUnit, [
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
def simple_expanded_memory_stream(simple_expanded_indexed_memory_stream: Iterable[IndexedMemoryUnit]) -> Iterable[int | None]:
    stream = (unit.file_id for unit in simple_expanded_indexed_memory_stream)
    return stream

@pytest.fixture
def simple_compressed_indexed_memory_stream() -> Iterable[IndexedMemoryUnit]:
    stream = starmap(IndexedMemoryUnit, [
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

@pytest.fixture
def simple_block_stream() -> Iterable[MemoryBlock]:
    stream = starmap(MemoryBlock, [
        (1, 0),
        (2, None),
        (3, 1),
        (4, None),
        (5, 2)
    ])

    return stream



def test_stream_block_pairs(simple_diskmap: str, simple_block_pair_stream: Iterable[BlockSizeAndID]):
    test = list(stream_block_pairs(simple_diskmap))
    reference = list(simple_block_pair_stream)
    assert test == reference

def test_parse_block_pair_to_blocks():
    file_size = 3
    free_size = 2
    file_id = 18

    reference = (MemoryBlock(file_size, file_id), MemoryBlock(free_size, None))
    test = parse_block_pair_to_blocks(BlockSizeAndID(file_size, free_size, file_id))

    assert test == reference


def test_stream_blocks(simple_diskmap: str, simple_block_stream: Iterable[MemoryBlock]):
    test = list(stream_blocks(simple_diskmap))
    reference = list(simple_block_stream)

    assert test == reference

def test_parse_memory_stream_to_blocks(
        simple_expanded_memory_stream: Iterable[int | None], simple_block_stream: Iterable[MemoryBlock]
):
    reference = list(simple_block_stream)
    test = list(
        parse_memory_stream_to_blocks(simple_expanded_memory_stream)
    )

    assert test == reference


def test_parse_block_pair():
    assert list(parse_block_pair(BlockSizeAndID(2, 3, 18))) == [
        18,
        18,
        None,
        None,
        None,
    ]


def test_parse_block_pairs_to_memory_stream(simple_block_pair_stream: Iterable[BlockSizeAndID], simple_expanded_indexed_memory_stream: Iterable[IndexedMemoryUnit]):
    reference = (m.file_id for m in simple_expanded_indexed_memory_stream)
    test = parse_block_pairs_to_memory_stream(
        simple_block_pair_stream
    )
    assert list(reference) == list(test)




def test_compress_memory_stream(
    example_expanded_memory: Iterable[int | None],
    example_compressed_memory: Iterable[int | None]
):
    reference = list(example_compressed_memory)
    test = list(compress_memory_stream(example_expanded_memory))
    assert reference == test


def test_find_checksum_from_memory_stream(
    example_compressed_memory: Iterable[int | None], example_final_checksum: int
):
    assert (
        find_checksum_from_memory_stream(example_compressed_memory)
        == example_final_checksum
    )

def test_find_checksum_from_memory_stream_part_2(
        example_fp_compressed_memory: Iterable[int | None],
        example_fp_final_checksum: int
):
    test = find_checksum_from_memory_stream(
        example_fp_compressed_memory
    )
    assert example_fp_final_checksum == test

def test_fp_compress_memory(
        example_expanded_memory: Iterable[int | None],
        example_fp_compressed_memory: Iterable[int | None]
):
    reference = list(example_fp_compressed_memory)
    test = list(
        fp_compress_memory(example_expanded_memory)
    )

    assert test == reference


def test_find_checksum(example_disk_map: str, example_final_checksum: int):
    assert find_checksum(example_disk_map) == example_final_checksum


def test_exercise_one_example(example_data_file: Path, example_final_checksum: int):
    assert exercise_one(example_data_file) == example_final_checksum


def test_exercise_one_real():
    assert exercise_one() == 6378826667552
