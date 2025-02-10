from pathlib import Path

DATA_DIR: Path = Path(__file__).parent
DATA_EXAMPLE_01: Path = DATA_DIR / "data_example_1.txt"
DATA_01: Path = DATA_DIR / "data_01.txt"

def import_rules(file_path: Path = DATA_01) -> dict[int, list[int]]:
    pass

def import_draft_page_lists(file_path: Path = DATA_01) -> list[list[int]]:
    pass

def exercise_one(file_path: Path = DATA_01) -> int:
    pass

if __name__ == "__main__":
    pass