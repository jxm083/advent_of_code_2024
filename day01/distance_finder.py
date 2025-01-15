import os
print(os.getcwd())

def import_data(file_name):
    """
    Takes in a file_name and returns two arrays of ints.
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


list_a = [3, 4, 2, 1, 3, 3]
list_b = [4, 3, 5, 3, 9, 3]

def sorted_list_difference(a, b):
    sorted_a = sorted(a)
    sorted_b = sorted(b)

    dif_ab = [abs(i - j) for (i,j) in zip(sorted_a, sorted_b)]

    return sum(dif_ab)

def calc_difference(file_name):
    data = import_data(file_name)
    diff = sorted_list_difference(data[0], data[1])
    return diff

print(import_data("numbers00.csv"))
print(sorted_list_difference(list_a, list_b))
print(calc_difference("numbers01.csv"))