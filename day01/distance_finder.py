list_a = [3, 4, 2, 1, 3, 3]
list_b = [4, 3, 5, 3, 9, 3]

def sorted_list_difference(a, b):
    sorted_a = sorted(a)
    sorted_b = sorted(b)

    dif_ab = [abs(i - j) for (i,j) in zip(sorted_a, sorted_b)]

    return sum(dif_ab)

print(sorted_list_difference(list_a, list_b))