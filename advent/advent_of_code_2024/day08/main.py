from math import sqrt

def distance(point0: tuple[int, int], point1: tuple[int, int]) -> float:
    return sqrt((point1[1] - point0[1]) ** 2 + (point1[0] - point0[0]) ** 2)

def exercise_one():
    pass

if __name__ == "__main__":
    print(f"exercise one: {exercise_one()}")