from pathlib import Path

DATA_DIR: Path = Path(__file__).parent
DATA_EXAMPLE_01: Path = DATA_DIR / "data_example_1.txt"
DATA_01: Path = DATA_DIR / "data_01.txt"

def parse_rule(line: str) -> tuple[int, int]:
    first, last = line.split("|")
    return int(first), int(last) # TODO: functional paradigm


def import_rules(file_path: Path = DATA_01) -> dict[int, list[int]]:
    """
    file_path (Path): the file path to the rules and page lists
    
    returns dict[int, list[int]]: a dictionary of entries of the form
    if KEY is in the page list, then none of the page numbers in
    VALUE's list may follow it."""
    rules: dict[int, list[int]] = dict()

    with file_path.open() as f:
        while line := f.readline().rstrip():
            count = line.count
            if count("|") == 1:
                first_num, last_num = parse_rule(line)
                if last_num in rules.keys():
                    rules[last_num].append(first_num)
                else:
                    rules[last_num] = [first_num]

    return rules

def import_page_lists(file_path: Path = DATA_01) -> list[list[int]]:
    page_lists: list[list[int]] = []

    with file_path.open() as f:
        for line in f.readlines():
            print(line)
            count = line.count
            if count(",") >= 1:
                page_lists.append([int(num) for num in line.split(",")])

    return page_lists

def valid_page_list(page_list: list[int], rules: dict[int, list[int]]) -> bool:
    """
    returns Boolean indicating whether list is valid
    """
    excluded_pages: list[int] = []
    valid_list: bool = True

    for page in page_list:
        if page in excluded_pages:
            valid_list = False
        else:
            if page in list(rules):
                excluded_pages.extend(rules[page])

    return valid_list

def exercise_one(file_path: Path = DATA_01) -> int:
    mid_num_sum: int = 0

    page_lists: list[list[int]] = import_page_lists(file_path)
    rules: dict[int, list[int]] = import_rules(file_path)

    for pages in page_lists:
        if valid_page_list(pages, rules):
            mid_num_sum += pages[len(pages)//2]

    return mid_num_sum

def exercise_two(file_path: Path = DATA_01) -> int:
    mid_num_sum: int = 0

    return mid_num_sum

if __name__ == "__main__":
    print(f"Exercise one: {exercise_one()}")