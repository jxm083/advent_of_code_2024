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

def cut_line_from_grid(grid: list[list[str]], length: int, direct: tuple[int, int]) -> list[str]:
    letters: list[str] = []

    for delta in range(length):
            letter: str = grid[-1 * direct[0] * delta][-1 * direct[1] * delta]
            letters.append(letter)

    return letters



def exercise_one(file_path: Path = DATA_P1) -> int:
    with file_path.open() as file:
        for line in file.readlines():
            print(line)

if __name__ == "__main__":
    print(generate_text_block(DATA_TEST, 2))
    exercise_one(DATA_TEST)