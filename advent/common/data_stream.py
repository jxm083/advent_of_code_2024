# Copied from Matt

from pathlib import Path
from typing import Generator, TypeVar, Callable

T = TypeVar("T")
U = TypeVar("U")


def stream_lines_from_file(f_path: Path) -> Generator[str, None, None]:
    with f_path.open() as f:
        while line := f.readline().rstrip():
            yield line

def parse_line_to_ints(line: str) -> Generator[int, None, None]:
    for i in line.split():
        yield int(i)

def pipe(
        in_stream: Generator[T, None, None],
        out_stream_gen: Callable[[T], Generator[U, None, None]]
) -> Generator[U, None, None]:
    for data in in_stream:
        yield from out_stream_gen(data)        