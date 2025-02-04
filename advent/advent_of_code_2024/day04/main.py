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
    




def exercise_one(file_path: Path = DATA_P1) -> int:
    with file_path.open() as file:
        for line in file.readlines():
            print(line)

if __name__ == "__main__":
    print(generate_text_block(DATA_TEST, 2))
    exercise_one(DATA_TEST)