from pathlib import Path
from collections import Counter
from typing import Callable

DATA_DIR = Path(__file__).parent
DATA_TEST = DATA_DIR / "data00.txt"
DATA_P1 = DATA_DIR / "data01.txt"

TARGET_STR = "XMAS"

def generate_text_block(file_path: Path, lin_count: int) -> list[str]:
    data: list[str] = []
    count = 0
    with file_path.open() as file:
        while count < lin_count:
            data.append(file.readline())
            count += 1

    return data
    
def convert_lines_to_grid(lines: list[str]) -> list[list[str]]:
    grid: list[list[str]] = []

    for line in lines:
        letters = [letter for letter in line]
        grid.append(letters.copy())

    return grid

def cut_line_from_grid(grid: list[list[str]], length: int, direct: tuple[int, int], center: tuple[int, int] = (0, 0)) -> list[str]:
    letters: list[str] = []

    for delta in range(length):
            x_ind = direct[0] * delta + center[0]
            y_ind = direct[1] * delta + center[1]
            letter: str = grid[y_ind][x_ind]
            letters.append(letter)

    return letters

def cut_x_from_grid(grid: list[list[str]], length: int, center: tuple[int, int] = (0, 0)) -> list[list[str]]:
    # the x is composed of two strokes
    # one starts at the top left and goes down, the other
    # starts at the top right and goes down
    stroke_one = cut_line_from_grid(grid, length, (1, 1), center=center)
    stroke_two = cut_line_from_grid(
        grid,
        length,
        (-1, 1)
        center=(center[0] + length - 1, center[1])
        )

    return [stroke_one, stroke_two]

def count_x_matches_from_grid_line(
        grid: list[list[str]],
        target: str 
) -> int:

    match_count: int = 0

    for letter_num, letter in enumerate(grid[0][:-len(target)]):
        if letter in [target[0], target[-1]]:
            strokes = cut_x_from_grid(grid, len(target), center = (letter_num, 0))
            count = Counter([str().join(stroke) for stroke in strokes])
            if sum([count[word] for word in [target, target[::-1]]]) == 2:
                match_count += 1

    return match_count

def count_matches_from_grid_line(
        grid: list[list[str]], 
        target: str = TARGET_STR
        ) -> int:
    
    match_count: int = 0

    for letter_num, letter in enumerate(grid[0][:]):
        if letter in [target[0], target[-1]]:
            cuts = cuts_at_letter(
                grid,
                letter_num,
                len(target)
            )
            cuts_counter = Counter([str().join(cut) for cut in cuts])
            match_count += cuts_counter[target] + cuts_counter[target[::-1]]
    
    return match_count

def cuts_at_letter(grid: list[list[str]], pos: int, length: int) -> list[list[str]]:
    """
    assumes the letter is in the top line of the grid and that 
    """
    # determine the directions in which cuts can be made
    directs: list[tuple[int, int]] = []
    if pos + length <= len(grid[0]):
        directs.append((1, 0))
        if length <= len(grid):
            directs.append((1, 1))
    if length <= len(grid):
        directs.append((0, 1))
        if length <= pos + 1:
            directs.append((-1, 1))

    cuts: list[list[str]] = []
    for direct in directs:
        cut = cut_line_from_grid(
            grid,
            length,
            direct,
            center=(pos, 0)
        )
        cuts.append(cut)

    return cuts

def count_matches_in_file(
        line_match_counter,
        target: str = TARGET_STR,
        file_path: Path = DATA_P1
        ) -> int:

        match_count: int = 0
        buffer: list[str] = []
        buffer_grid: list[list[str]] = []

        with file_path.open() as file:
            for line_num, line in enumerate(file.readlines()):
                if line_num >= len(target) - 1:
                    buffer_grid = convert_lines_to_grid(buffer)
                    match_count += line_match_counter(
                        buffer_grid,
                        target
                    )
                    del buffer[0]
        
        for ind in range(len(buffer_grid) - 1):
            match_count += line_match_counter(
                buffer_grid[ind + 1:],
                target
            )
        
        return match_count



def exercise_one(file_path: Path = DATA_P1) -> int:
    buffer: list[str] = []
    buffer_grid: list[list[str]] = []
    word_count: int = 0

    with file_path.open() as file:
        for line_num, line in enumerate(file.readlines()):
            buffer.append(line.rstrip())
            if line_num >= len(TARGET_STR) - 1:
                buffer_grid = convert_lines_to_grid(buffer)
                word_count += count_matches_from_grid_line(
                    buffer_grid,
                    target=TARGET_STR
                )
                del buffer[0]
        # Need to search the remainder of the buffer

    for ind in range(len(buffer_grid) - 1):
        word_count += count_matches_from_grid_line(
            buffer_grid[ind + 1:],
            target=TARGET_STR
        )
    
    return word_count

def exercise_two(file_path: Path = DATA_P1) -> int:
    buffer: list[str] = []


if __name__ == "__main__":
    print(f"Number of matches {exercise_one()}")