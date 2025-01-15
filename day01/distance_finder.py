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

def sorted_list_difference(a, b):
    sorted_a = sorted(a)
    sorted_b = sorted(b)

    dif_ab = [abs(i - j) for (i,j) in zip(sorted_a, sorted_b)]

    return sum(dif_ab)

def calc_difference(file_name):
    data = import_data(file_name)
    diff = sorted_list_difference(data[0], data[1])
    return diff

def calc_similiarity(file_name):
    data = import_data(file_name)
    weighted_score = [ num * data[1].count(num) for num in data[0] ]
    return sum(weighted_score)

print(f"List total difference: {calc_difference("numbers01.csv")}")
print(f"List similiarity: {calc_similiarity("numbers01.csv")}")