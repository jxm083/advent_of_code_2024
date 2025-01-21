def import_data(file_name: str) -> list:
    """
    Takes in a file_name and returns two arrays of ints.
    Must be run in the same directory as the data.

    Assumes that each line of the file corresponds to the entries
    of all the individual lists, separated by spaces.

    Args:
        file_name (str): name of file containing list of location ints

    Returns:
        list: A list of the location int lists
    """
    file = open(file_name, "r")
    numbers_all = []

    for line in file.readlines():
        line.strip() # remove leading and trailing spaces
        nums = line.split(" ")
        nums_clean = [int(num.strip()) for num in nums if num != '']
        numbers_all.append(nums_clean)
        
    # Reshape so that each element of data is a column of the original file
    data = [[nums[i] for nums in numbers_all] for i in range(len(numbers_all[0]))]

    return data

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

def exercise_one(file_name: str | None = "numbers01.csv") -> int:
    # Pull the data in from the file
    data = import_data(file_name)

    # sort the lists
    list_a = sorted(data[0])
    list_b = sorted(data[1])

    # calculate the difference
    return calc_difference(list_a, list_b)

def exercise_two(file_name: str | None = "numbers01.csv") -> int:
    # Pull the data from the file
    data = import_data(file_name)

    return calc_similiarity(data[0], data[1])

if __name__ == "__main__":
    print(f"List total difference: {exercise_one()}")
    print(f"List similiarity: {exercise_two()}")