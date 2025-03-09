import pytest
from advent.common.vectors import (
    Vector,
    vec_add,
    vec_mul,
    vec_dot
)

@pytest.fixture
def vec0():
    return Vector([1, 2, 3])

@pytest.fixture
def vec1():
    return Vector([-1, -2, -3])

def test_length(vec0: Vector):
    assert vec0.length() == 14

def test_vector_not_equal(vec0: Vector, vec1: Vector):
    assert vec0.components != vec1.components

def test_vector_addition(vec0: Vector, vec1: Vector):
    assert vec_add(vec0, vec1).components == Vector([0, 0, 0]).components

def test_scalar_multiplication():
    fac: int = 3
    vec: Vector = Vector([1, 4])

    assert vec_mul(fac, vec).components == Vector([3, 12]).components

def test_dot_product(vec0: Vector, vec1: Vector):
    assert vec_dot(vec0, vec1) == -14


if __name__ == "__main__":
    vec_0 = Vector([1, 2, 3])
    vec_1 = Vector([-1, -2 , -3])

    print(1 + 3)
    print(vec_0 + vec_1)
    print(vec_0)