from pathlib import Path

DATA_DIR: Path = Path(__file__).parent
DATA_EXAMPLE_01: Path = DATA_DIR / "data_example_1.txt"
DATA_01: Path = DATA_DIR / "data_01.txt"

def parse_rule(line: str) -> tuple[int, int]:
    first, last = line.split("|")
    return int(first), int(last) # TODO: functional paradigm


def import_rules(file_path: Path = DATA_01) -> dict[int, list[int]]:
    rules: dict[int, list[int]] = dict()

    with file_path.open() as f:
        while line := f.readline().rstrip():
            count = line.count
            if count("|") == 1:
                first_num, last_num = parse_rule(line)
                if first_num in rules.keys():
                    rules[first_num].append(last_num)
                else:
                    rules[first_num] = [last_num]

    return rules

def import_draft_page_lists(file_path: Path = DATA_01) -> list[list[int]]:
    draft_page_lists: list[list[int]] = []

    with file_path.open() as f:
        for line in f.readlines():
            print(line)
            count = line.count
            if count(",") >= 1:
                draft_page_lists.append([int(num) for num in line.split(",")])

    return draft_page_lists

def exercise_one(file_path: Path = DATA_01) -> int:
    pass

if __name__ == "__main__":
    pass