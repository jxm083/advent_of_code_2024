from itertools import groupby, count, batched
from pathlib import Path

from advent.common.data_stream import stream_lines_from_file

DATA_DIR = Path(__file__).parent
EXAMPLE_DATA_PATH = DATA_DIR / "data_example.txt"

def create_file_block(block_size: int, block_id: int) -> str:
    return block_size * str(block_id)


def create_free_block(block_size: int) -> str:
    return block_size * "."

def parse_diskmap_pairs(diskmap: str):
    # To send out pairs of file_block_size and free_block_size
    # the amount of free space after the last file 
    # has to be padded
    free_space_after_last_file = "0"
    diskmap_pairs = batched(
        diskmap + free_space_after_last_file, 
        n=2)

    for file_block_size, free_block_size in diskmap_pairs:
        yield file_block_size, free_block_size


def create_file_free_pair(
    file_block_size: str, free_block_size: str, block_id: int
) -> str:
    file_block = create_file_block(int(file_block_size), block_id)
    free_block = create_free_block(int(free_block_size))
    return file_block + free_block


def expand_diskmap(diskmap: str):
    for block_id, file_block_size, free_block_size in parse_diskmap(diskmap):
        yield create_file_free_pair(file_block_size, free_block_size, block_id)
        

def find_checksum_from_expanded_diskmap():
    pass

def find_checksum():
    pass


def exercise_one():
    pass


if __name__ == "__main__":
    EXAMPLE_DISKMAP = "2333133121414131402"
    print(list(parse_diskmap_pairs(EXAMPLE_DISKMAP)))
    # print(list(expand_diskmap(EXAMPLE_DISKMAP + "0")))
