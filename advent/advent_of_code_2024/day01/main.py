from pathlib import Path

from advent.common.import_data import import_data, transpose_data

def calc_difference(list_a: list[int], list_b: list[int]) -> int:
    """Return the summed distance between elements.
    
    This assumes both lists are sorted.
    
    distance is defined to be the difference between the two numbers.
    
    Args:
        list_a (list[int]): sorted location ints
        list_b (list[ing]): sorted location ints
    
    Returns:
        int: pair-wise sum of elements
    """
    diff_ab = [abs(i - j) for (i,j) in zip(list_a, list_b)]

    return sum(diff_ab)

def calc_similiarity(list_a: list[int], list_b: list[int]) -> int:
    """Calculate similiarity of two lists of ints, as defined by
    frequency_in_list2 * value * frequency_in_list_1
    
    Args:
        list_a (list[int]): location ints
        list_b (list[int]): location ints
        
    Returns:
        int: pair-wise sume of elements
    """
    weighted_score = [ num * list_b.count(num) for num in list_a ]
    return sum(weighted_score)

DATA_DIR = Path(__file__).parents[0]

def exercise_one(file_name: str | None = "numbers01.csv") -> int:
    # Pull the data in from the file
    data = import_data(file_name, file_dir = DATA_DIR) # type: ignore
    data = transpose_data(data)

    # sort the lists
    list_a = sorted(data[0])
    list_b = sorted(data[1])

    # calculate the difference
    return calc_difference(list_a, list_b)

def exercise_two(file_name: str | None = "numbers01.csv") -> int:
    # Pull the data from the file
    data = import_data(file_name, file_dir = DATA_DIR) # type: ignore
    data = transpose_data(data)

    return calc_similiarity(data[0], data[1])

if __name__ == "__main__":
    print(f"List total difference: {exercise_one()}")
    print(f"List similiarity: {exercise_two()}")