def import_data(file_name):
    """
    Takes in a file_name and returns two arrays of ints.
    Must be run in the same directory as the data.
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
    # assume that the lists are already sorted
    diff_ab = [abs(i - j) for (i,j) in zip(list_a, list_b)]

    return sum(diff_ab)

def calc_similiarity(file_name):
    data = import_data(file_name)
    weighted_score = [ num * data[1].count(num) for num in data[0] ]
    return sum(weighted_score)

def exercise_one(file_name: str | None = "numbers01.csv") -> int:
    # Pull the data in from the file
    data = import_data(file_name)

    # sort the lists
    list_a = sorted(data[0])
    list_b = sorted(data[1])

    # calculate the difference
    return calc_difference(list_a, list_b)

if __name__ == "__main__":
    print(f"List total difference: {exercise_one()}")
    print(f"List similiarity: {calc_similiarity("numbers01.csv")}")