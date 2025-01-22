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
    print(file_dir)
    file_path = file_dir / Path(file_name)
    numbers_all = []

    with file_path.open() as file:

        for line in file.readlines():
            line.strip() # remove leading and trailing spaces
            nums = line.split(" ")
            nums_clean = [int(num.strip()) for num in nums if num != '']
            numbers_all.append(nums_clean)
        
    # Reshape so that each element of data is a column of the original file
    data = [[nums[i] for nums in numbers_all] for i in range(len(numbers_all[0]))]

    return data