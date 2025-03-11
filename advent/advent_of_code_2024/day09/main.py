def create_file_block(block_size: int, block_id: int) -> str:
    return block_size * str(block_id)


def create_free_block(block_size: int) -> str:
    return block_size * "."


def parse_file_free_pair(
    file_block_size: int, free_block_size: int, block_id: int
) -> str:
    file_block = create_file_block(file_block_size, block_id)
    free_block = create_free_block(free_block_size)
    return file_block + free_block


def expand_diskmap(diskmap: str):
    pass


def find_checksum():
    pass


def exercise_one():
    pass


if __name__ == "__main__":
    pass
