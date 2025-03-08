# Copied from Matt

from pathlib import Path
from typing import Generator, TypeVar, Callable, Iterator, TypeAlias

T = TypeVar("T")
U = TypeVar("U")

CharData: TypeAlias = tuple[int, int, str]


def stream_lines_from_file(f_path: Path) -> Generator[str, None, None]:
    with f_path.open() as f:
        while line := f.readline():
            yield line.rstrip()

def parse_line_to_ints(line: str) -> Generator[int, None, None]:
    for i in line.split():
        yield int(i)

def pipe(
        in_stream: Generator[T, None, None],
        out_stream_gen: Callable[[T], Generator[U, None, None]]
) -> Generator[U, None, None]:
    for data in in_stream:
        yield from out_stream_gen(data)        

def stream_position_and_char(
    file_data: Iterator[str],
) -> Iterator[CharData]:  # TODO: move this to common
    for line_num, line in enumerate(file_data):
        for char_num, char in enumerate(line):
            yield (line_num, char_num, char)