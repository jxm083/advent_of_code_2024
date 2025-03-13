from itertools import count, batched
from typing import Iterator, NamedTuple, Iterable
from pathlib import Path

from advent.common.extended_itertools import flatten
from advent.common.data_stream import stream_lines_from_file


class BlockSizeAndID(NamedTuple):
    file_block_size: int
    free_block_size: int
    id: int

class MemoryBlock(NamedTuple):
    contents: str
    id: int


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

def translate_memory_string_to_file_id_stream(expanded_diskmap_str: str) -> Iterator[int | None]:
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


def parse_block_pairs_to_memory_stream(block_pairs: Iterable[BlockSizeAndID]) -> Iterator[MemoryBlock]:
    pass


def stream_diskmap(diskmap: str) -> Iterator[BlockSizeAndID]:
    diskmap_pairs = map(fill_in_pair, batched(map(int, diskmap), n=2))

    for id, (file_size, free_size) in enumerate(diskmap_pairs):
        yield BlockSizeAndID(file_size, free_size, id)


# TODO: type-safe way to generalize this with default value?
def expand_diskmap(diskmap: str) -> Iterable[str]:
    return flatten(map(create_file_free_pair, stream_diskmap(diskmap)))

def stream_character_and_id(string: str) -> Iterator[tuple[int, str]]:
    for num, char in enumerate(string):
        yield (num, char)

def get_next_compressed_block() -> Iterator[int]:
    pass

def compress_expanded_diskmap(expanded_diskmap: Iterable[str]) -> Iterable[str]:
    indexed_diskmap = [(ind, char) for ind, char in zip(count(), expanded_diskmap)]
    reversed_indexed_diskmap = iter(indexed_diskmap[::-1])
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
def find_checksum_from_compressed_diskmap(compressed_diskmap: str) -> int:
    total = 0
    for id, char in enumerate(compressed_diskmap):
        if char == ".":
            break
        else:
            total += id * int(char)
    return total


def find_checksum(diskmap: str) -> int:
    expanded_diskmap = expand_diskmap(diskmap)
    compressed_diskmap = compress_expanded_diskmap(expanded_diskmap)
    checksum = find_checksum_from_compressed_diskmap(compressed_diskmap)
    return checksum


def exercise_one(file_path: Path = DATA_PATH) -> int:
    file_stream = stream_lines_from_file(file_path)
    diskmap = next(file_stream)
    return find_checksum(diskmap)


if __name__ == "__main__":
    print(f"exercise one: {exercise_one()}")
    EXAMPLE_DISKMAP = "2333133121414131402"
    EXPANDED_DISKMAP = expand_diskmap(EXAMPLE_DISKMAP)
    print()
    # print(list(parse_diskmap_pairs(EXAMPLE_DISKMAP)))
    # print(list(expand_diskmap(EXAMPLE_DISKMAP)))
    # print(list(expand_diskmap("12345")))
