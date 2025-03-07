from advent.common.extended_itertools import takewhile_pair

def test_takewhile_pair():
    reference = [0, -1, 1, -2, 2]
    test_sequence = [0, -1, 1, -2, 2, -3, -4]

    def gt0(x: int) -> bool:
        return x >= 0

    assert list(takewhile_pair(gt0, [0, 1])) == [0, 1]

    assert list(takewhile_pair(gt0, test_sequence)) == reference

def test_takewhile_pair_edge_cases():
    def gt0(x: int) -> bool:
        return x >= 0

    assert list(takewhile_pair(gt0, [])) == []