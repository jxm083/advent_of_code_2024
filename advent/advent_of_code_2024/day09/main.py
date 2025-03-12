from itertools import groupby, count, batched
from typing import Iterator, TypeAlias, NamedTuple
from pathlib import Path

from advent.common.data_stream import stream_lines_from_file


class BlockSizeAndID(NamedTuple):
    file_block_size: int
    free_block_size: int
    id: int


DATA_DIR = Path(__file__).parent
EXAMPLE_DATA_PATH = DATA_DIR / "data_example.txt"


# TODO: type-safe way to generalize this with default value?
def fill_in_pair(
    possible_pair: tuple[int, ...], fill_value: int = 0
) -> tuple[int, int]:
    if len(possible_pair) == 2:
        pair = possible_pair
    else:
        pair = (possible_pair[0], fill_value)

    return pair


def create_file_block(block_size: int, block_id: int) -> str:
    return block_size * str(block_id)


def create_free_block(block_size: int) -> str:
    return block_size * "."


def create_file_free_pair(block_data: BlockSizeAndID) -> str:
    file_block = create_file_block(block_data.file_block_size, block_data.id)
    free_block = create_free_block(block_data.free_block_size)
    return file_block + free_block


def stream_diskmap(diskmap: str) -> Iterator[BlockSizeAndID]:
    diskmap_pairs = map(fill_in_pair, batched(map(int, diskmap), n=2))

    for id, (file_size, free_size) in enumerate(diskmap_pairs):
        yield BlockSizeAndID(file_size, free_size, id)


# TODO: type-safe way to generalize this with default value?
def expand_diskmap(diskmap: str) -> str:
    return str.join("", map(create_file_free_pair, stream_diskmap(diskmap)))

def stream_character_and_id(string: str) -> Iterator[tuple[int, str]]:
    for num, char in enumerate(string):
        yield (num, char)
    

def compress_expanded_diskmap(expanded_diskmap: str) -> str:
    indexed_diskmap = [(ind, char) for ind, char in zip(count(), expanded_diskmap)]
    reversed_indexed_diskmap = iter(indexed_diskmap[::-1])
    compressed_diskmap = str()
    back_ind: int | None = None
    for ind, char in indexed_diskmap:
        if ind == back_ind:
            break
        elif char != ".":
            compressed_diskmap += char
        else:
            back_char = "."
            while back_char == ".":
                back_ind, back_char = next(reversed_indexed_diskmap)
                if back_ind == ind:
                    break
            compressed_diskmap += back_char

    return compressed_diskmap.ljust(len(expanded_diskmap), ".")


    


# TODO: do with filter, map, and count
def find_checksum_from_compressed_diskmap(compressed_diskmap: str) -> int:
    total = 0
    for id, char in enumerate(compressed_diskmap):
        if char == ".":
            break
        else:
            total += id * int(char)
    return total


def find_checksum():
    pass


def exercise_one():
    pass


if __name__ == "__main__":
    EXAMPLE_DISKMAP = "2333133121414131402"
    print(compress_expanded_diskmap("0..111....22222"))
    # print(list(parse_diskmap_pairs(EXAMPLE_DISKMAP)))
    # print(list(expand_diskmap(EXAMPLE_DISKMAP)))
    # print(list(expand_diskmap("12345")))
