from itertools import count, batched, chain
from typing import Iterator, NamedTuple, Iterable
from pathlib import Path

from advent.common.extended_itertools import flatten
from advent.common.data_stream import stream_lines_from_file


class BlockSizeAndID(NamedTuple):
    file_block_size: int
    free_block_size: int
    file_id: int


class MemoryBlock(NamedTuple):
    memory_ind: int
    file_id: int | None


DATA_DIR = Path(__file__).parent
EXAMPLE_DATA_PATH = DATA_DIR / "data_example.txt"
DATA_PATH = DATA_DIR / "data.txt"


# TODO: type-safe way to generalize this with default value?
def fill_in_pair(
    possible_pair: tuple[int, ...], fill_value: int = 0
) -> tuple[int, int]:
    if len(possible_pair) == 2:
        pair = possible_pair
    else:
        pair = (possible_pair[0], fill_value)

    return pair


def translate_memory_string_to_file_id_stream(
    expanded_diskmap_str: str,
) -> Iterator[int | None]:
    """
    NOTE: This only works when the memory blocks in the expanded
    diskmap have single-digit IDs
    """
    for char in expanded_diskmap_str:
        if char == ".":
            yield None
        else:
            yield int(char)


def translate_file_id_to_str(memory_id: int | None) -> str:
    char: str | None = None
    if memory_id is None:
        char = "."
    else:
        char = str(memory_id)
    return char


def translate_file_id_stream_to_memory_string(id_stream: Iterable[int | None]) -> str:
    """
    NOTE: This only works when the memory blocks in the diskmap
    have singe-digit IDs
    """
    return "".join(map(translate_file_id_to_str, id_stream))


def parse_block_pair(block_pair: BlockSizeAndID) -> Iterable[int | None]:
    file_block = block_pair.file_block_size * [block_pair.file_id]
    memory_block = block_pair.free_block_size * [None]
    return chain(file_block, memory_block)


def stream_diskmap(diskmap: str) -> Iterator[BlockSizeAndID]:
    diskmap_pairs = map(fill_in_pair, batched(map(int, diskmap), n=2))

    for id, (file_size, free_size) in enumerate(diskmap_pairs):
        yield BlockSizeAndID(file_size, free_size, id)

def parse_block_pairs_to_indexed_memory_stream(
    block_pairs: Iterable[BlockSizeAndID],
) -> Iterator[int | None]:
    for pair in block_pairs:
        block = parse_block_pair(pair)
        for unit in block:
            yield unit



def fill_memory(current_memory_cell: tuple[int, int], fill_values: Iterable[tuple[int, int]]) -> int | None:
    fill_index, fill_value = next(fill_values)
    if current_memory_cell[0] >= fill


def compress_memory_stream(memory_stream: Iterable[int | None]) -> Iterable[int | None]:
    indexed_memory = list(enumerate(memory_stream))
    fill_values = filter(lambda x: x[1] is not None, iter(indexed_memory[::-1]))
    compressed_diskmap = str()
    back_ind: int | None = None
    for ind, char in indexed_diskmap:
        if back_ind is not None and back_ind <= ind:
            break
        elif char != ".":
            compressed_diskmap += char
        else:
            back_char = "."
            while back_char == ".":
                back_ind, back_char = next(reversed_indexed_diskmap)
                if back_ind <= ind:
                    break
            compressed_diskmap += back_char

    return compressed_diskmap.ljust(len(indexed_diskmap), ".")


# TODO: do with filter, map, and count
def find_checksum_from_compressed_memory_stream(compressed_memory_stream: Iterable[int | None]) -> int:
    total = 0
    for ind, file_id in enumerate(compressed_memory_stream):
        if file_id is None:
            break
        else:
            total += ind * file_id

    return total


def find_checksum(diskmap: str) -> int:
    pass


def exercise_one(file_path: Path = DATA_PATH) -> int:
    file_stream = stream_lines_from_file(file_path)
    diskmap = next(file_stream)
    return find_checksum(diskmap)


if __name__ == "__main__":
    print(f"exercise one: {exercise_one()}")
    EXAMPLE_DISKMAP = "2333133121414131402"
    print()
    # print(list(parse_diskmap_pairs(EXAMPLE_DISKMAP)))
    # print(list(expand_diskmap(EXAMPLE_DISKMAP)))
    # print(list(expand_diskmap("12345")))
