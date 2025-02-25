from pathlib import Path
from typing import TypeAlias

DATA_DIR = Path(__file__).parent
EXAMPLE_DATA = DATA_DIR / "data00.txt"


Equation: TypeAlias = tuple[int, tuple[int,...]]
def parse_equation(line: str) -> Equation:
    pass

def exercise_one(data_path: Path) -> int:
    pass

if __name__ == "__main__":
    pass