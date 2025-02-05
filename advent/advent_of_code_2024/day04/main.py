from pathlib import Path

DATA_DIR = Path(__file__).parent
DATA_TEST = DATA_DIR / "data00.txt"
DATA_P1 = DATA_DIR / "data01.txt"

TARGET_STR = "XMAS"

def text_line(
        data: list[str], 
        position: tuple[int, int],
        direction: tuple[int, int], 
        length: int
    ) -> str:

    pass

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
            y_ind = -1 * direct[1] * delta + center[1]
            letter: str = grid[y_ind][x_ind]
            letters.append(letter)

    return letters



def exercise_one(file_path: Path = DATA_P1) -> int:
    buffer: list[str] = []
    buffer_grid: list[list[str]] = []
    word_count: int = 0

    with file_path.open() as file:
        for line_num, line in enumerate(file.readlines()):
            buffer.append(line.rstrip())
            if line_num >= len(TARGET_STR) - 1:
                buffer_grid = convert_lines_to_grid(buffer)

                print(buffer_grid)
                del buffer[0]

            print(line_num, line)

if __name__ == "__main__":
    print(generate_text_block(DATA_TEST, 2))
    exercise_one(DATA_TEST)