import pytest
from advent.common.vectors import (
    Vector,
)

@pytest.fixture
def vec0():
    return Vector([1, 2, 3])

@pytest.fixture
def vec1():
    return Vector([-1, -2, -3])

def test_magnitude(vec0: Vector):
    assert vec0.magnitude() == 14

def test_vector_get_item(vec0: Vector):
    assert vec0[0] == 1
    assert vec0[1] == 2
    assert vec0[2] == 3

def test_vector_not_equal(vec0: Vector, vec1: Vector):
    assert vec0 != vec1

def test_vector_equal(vec0: Vector):
    assert vec0 == Vector([1, 2, 3])

def test_vector_addition(vec0: Vector, vec1: Vector):
    assert vec0 + vec1 == Vector([0, 0, 0])

def test_vector_subtraction(vec0: Vector, vec1: Vector):
    assert vec0 - vec1 == Vector([2, 4, 6])

def test_scalar_multiplication():
    fac: int = 3
    vec: Vector = Vector([1, 4])

    assert vec * fac == Vector([3, 12])

    assert fac * vec == Vector([3, 12])

def test_dot_product(vec0: Vector, vec1: Vector):
    assert vec0.dot(vec1) == -14

def test_negative(vec0: Vector):
    assert -vec0 == Vector([-1, -2, -3])


if __name__ == "__main__":
    vec_0 = Vector([1, 2, 3])
    vec_1 = Vector([-1, -2 , -3])
    vec_0[0] = 2
    print(vec_0)

    print(1 + 3)
    print(vec_0 + vec_1)
    print(vec_0)