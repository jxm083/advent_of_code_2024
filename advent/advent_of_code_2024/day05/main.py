from pathlib import Path
import re
from typing import Generator, Iterator

from advent.common.data_stream import stream_lines_from_file

DATA_DIR: Path = Path(__file__).parent
DATA_EXAMPLE_01: Path = DATA_DIR / "data_example_1.txt"
DATA_01: Path = DATA_DIR / "data_01.txt"

RULE_PATTERN = re.compile(r"(\d+)\| ?(\d+)")
PAGE_LIST_PATTERN = re.compile(r"(\d+),")

# TODO: break into separate stream and parse functions?
def stream_rules(data: str, rule_pattern: re.Pattern[str] = RULE_PATTERN) -> Generator[tuple[int, int], None, None]:
    for match in re.finditer(rule_pattern, data):
        g = match.groups()
        yield (int(g[0]), int(g[1]))
    
def compile_rule_dict(file_path: Path = DATA_01) -> dict[int, list[int]]:
    rule_dict:  dict[int, list[int]] = dict()

    data_stream = stream_rules(file_path.read_text())

    for pred, post in data_stream:

        if post in rule_dict.keys():
            rule_dict[post].append(pred)

        else:
            rule_dict[post] = [pred]

    return rule_dict

def import_page_lists(file_path: Path = DATA_01) -> list[list[int]]:
    page_lists: list[list[int]] = []

    with file_path.open() as f:
        for line in f.readlines():
            count = line.count
            if count(",") >= 1:
                page_lists.append([int(num) for num in line.split(",")])

    return page_lists

def is_page_list(text: str, page_list_pattern: re.Pattern[str] = PAGE_LIST_PATTERN) -> bool:
    return bool(page_list_pattern.search(text))

def parse_list(text: str) -> list[int]:
    page_split: str = r"\d+"
    
    page_list = [int(match) for match in re.findall(page_split, text)]

    return page_list

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

def sum_median_values(values_list: Iterator[list[int]]) -> int:
    return sum(values[len(values)//2] for values in values_list)

def exercise_one(file_path: Path = DATA_01) -> int:
    rules: dict[int, list[int]] = compile_rule_dict(file_path)
    file_stream = stream_lines_from_file(file_path)

    page_lists = map(
        parse_list,
        filter(is_page_list, file_stream)
    )
    
    valid_page_lists = filter(
        lambda x: valid_page_list(x, rules),
        page_lists
        )

    return sum_median_values(valid_page_lists)

def reorder_pages_pass(pages: list[int], rules: dict[int, list[int]]) -> list[int]:
    new_pages: list[int] = pages

    for ind, page in enumerate(pages):
        if page in list(rules) and not valid_page_list(pages[ind:], rules):
            predecessor_inds: list[int] = []
            for predecessor in rules[page]:
                if predecessor in pages[ind + 1:]:
                    predecessor_inds.append(pages.index(predecessor))
            
            if predecessor_inds:
                last_predecessor_ind: int = max(predecessor_inds)

                new_pages.insert(last_predecessor_ind + 1, page)
                new_pages.pop(ind)

    return new_pages

def reorder_pages(pages: list[int], rules: dict[int, list[int]]) -> list[int]:
    new_pages: list[int] = pages

    while not valid_page_list(new_pages, rules):
        new_pages = reorder_pages_pass(new_pages, rules)

    return new_pages

def exercise_two(file_path: Path = DATA_01) -> int:
    file_stream = stream_lines_from_file(file_path)
    page_lists = map(
        parse_list,
        filter(is_page_list, file_stream)
    )

    rules: dict[int, list[int]] = compile_rule_dict(file_path)

    corrected_page_lists = map(
        lambda x: reorder_pages(x, rules),
        filter(
            lambda x: not(valid_page_list(x, rules)),
            page_lists
        )
    )

    return sum_median_values(corrected_page_lists)

if __name__ == "__main__":
    print(f"Exercise one: {exercise_one()}")
    print(f"Exercise two: {exercise_two()}")