import pytest

from advent.advent_of_code_2024.day03.main import exercise_one

@pytest.fixture
def test_line() -> str:
    test_line = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    return test_line

def test_exercise_one():
    exercise_one()