from pathlib import Path
import os

def import_data(file_name: str, file_dir: Path = Path(os.getcwd())) -> list:
    """
    Takes in a file_name and returns two arrays of ints.
    Must be run in the same directory as the data.

    Assumes that each line of the file corresponds to the entries
    of all the individual lists, separated by spaces.

    Args:
        file_name (str): name of file containing list of location ints
        file_dir (Path): a path object specifying the directory containing the file; defaults to current working directory

    Returns:
        list: A list of the location int lists
    """
    file_path = file_dir / Path(file_name)
    data = []

    with file_path.open() as file:

        for line in file.readlines():
            line.strip() # remove leading and trailing spaces
            nums = line.split(" ")
            nums_clean = [int(num.strip()) for num in nums if num != '']
            data.append(nums_clean)

    return data

def transpose_data(data: list):
    """
    Transposes two dimensional lists, e.g.

    [[a, b, c], [d, e, f]]

    becomes

    [[a, d], [b, e], [c, f]] .

    Assumes lists of depth two, each nested list being of the same dimension

    Args:
        data (list): A depth-two list

    Returns:
        list: the list with the axes swapped
    """
    # Reshape so that each element of data is a column of the original file
    return [[nums[i] for nums in data] for i in range(len(data[0]))]
