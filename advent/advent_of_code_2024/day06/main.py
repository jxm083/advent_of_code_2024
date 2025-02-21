from typing import Generator, Iterator

def parse_lines_to_grid_entries(file_stream: Generator[str, None, None]) -> Iterator[tuple[int, int, str]]:
    for line_num, line in enumerate(file_stream):
        for char_num, character in enumerate(line):
            yield (line_num, char_num, character)

if __name__ == "__main__":
    pass