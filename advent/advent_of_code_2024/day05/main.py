from pathlib import Path
import re
from typing import Generator, Iterator, Callable

from advent.common.data_stream import stream_lines_from_file

DATA_DIR: Path = Path(__file__).parent
DATA_EXAMPLE_01: Path = DATA_DIR / "data_example_1.txt"
DATA_01: Path = DATA_DIR / "data_01.txt"

RULE_PATTERN = re.compile(r"(\d+)\| ?(\d+)")
PAGE_LIST_PATTERN = re.compile(r"(\d+),")

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

def import_page_list(file_stream: Generator[str, None, None]) -> Generator[list[int], None, None]:
    for line in file_stream:
        if is_page_list(line):
            yield parse_list(line)

def sum_median_values(values_list: Iterator[list[int]]) -> int:
    return sum(values[len(values)//2] for values in values_list)

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

def process_updates(
    file_path: Path,
    page_list_selector: Callable[[list[int], dict[int, list[int]]], bool],
    page_list_manipulator: Callable[[list[int], dict[int, list[int]]], list[int]] | None,
    page_list_condensor: Callable[[Iterator[list[int]]], int]
) -> int:
    rules = compile_rule_dict(file_path)

    file_stream = stream_lines_from_file(file_path)
    page_lists = import_page_list(file_stream)

    selected_page_lists = filter(
        lambda x: page_list_selector(x, rules),
        page_lists
    )

    if page_list_manipulator is not None:
        processed_page_lists = map(
            lambda x: page_list_manipulator(x, rules),
            selected_page_lists
        )
    else:
        processed_page_lists = selected_page_lists


    return page_list_condensor(processed_page_lists)

def exercise_one(file_path: Path = DATA_01) -> int:
    return process_updates(
        file_path,
        page_list_selector=valid_page_list,
        page_list_manipulator=None,
        page_list_condensor=sum_median_values
    )

def exercise_two(file_path: Path = DATA_01) -> int:
    return process_updates(
        file_path,
        page_list_selector=(lambda x, y: not(valid_page_list(x, y))),
        page_list_manipulator=reorder_pages,
        page_list_condensor=sum_median_values
    )

if __name__ == "__main__":
    print(f"Exercise one: {exercise_one()}")
    print(f"Exercise two: {exercise_two()}")