from typing import Generator, Iterator
from pathlib import Path

DATA_DIR = Path(__file__).parent
DATA_00_Path = DATA_DIR / "data_00.txt"
DATA_01_PATH = DATA_DIR / "data_01.txt"

def parse_lines_to_grid_entries(file_stream: Generator[str, None, None]) -> Iterator[tuple[int, int, str]]:
    for line_num, line in enumerate(file_stream):
        for char_num, character in enumerate(line):
            yield (line_num, char_num, character)

def calc_next_step(location: tuple[int, int], direction: tuple[int, int], map_dict: dict[tuple[int, int], str]) -> tuple[int, int] | None:
    loc_x: int = location[0] + direction[0]
    loc_y: int = location[0] + direction[0]

    loc: tuple[int, int] = (loc_x, loc_y)

    if loc in map_dict.keys:
        pass
    else:
        return None

def exercise_one(file_path: Path = DATA_01_PATH):
    pass

if __name__ == "__main__":
    pass