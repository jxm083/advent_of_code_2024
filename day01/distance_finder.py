import os
print(os.getcwd())

def import_nums(file_name):
    """
    Takes in a file_name and returns two arrays of ints.
    """
    file = open(file_name, "r")
    numbers_all = []

    for line in file.readlines():
        line.strip() # remove leading and trailing spaces
        nums = line.split(" ")
        nums_clean = [int(num.strip()) for num in nums if num != '']
        print(nums_clean)
        numbers_all.append(nums_clean)

    return numbers_all


list_a = [3, 4, 2, 1, 3, 3]
list_b = [4, 3, 5, 3, 9, 3]

def sorted_list_difference(a, b):
    sorted_a = sorted(a)
    sorted_b = sorted(b)

    dif_ab = [abs(i - j) for (i,j) in zip(sorted_a, sorted_b)]

    return sum(dif_ab)

print()
print(import_nums("numbers00.csv"))
print(sorted_list_difference(list_a, list_b))