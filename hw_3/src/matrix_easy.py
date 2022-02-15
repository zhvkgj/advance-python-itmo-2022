#!/usr/bin/python3
from operator import add, mul
from typing import List

from hw_3.src.matrix_common import AsListMixin, PersistentMixin, UtilityMixin


class Matrix(AsListMixin, PersistentMixin, UtilityMixin):
    def __init__(self, data: List[List[int]]):
        self._data = data

    def _assert_dims(self, other: 'Matrix', is_total=False):
        n, m = self.shape
        k, p = other.shape
        if is_total:
            if n != k or m != p:
                raise ValueError(f"Matrices with incompatible shapes for element-wise operation")
        elif n != m:
            raise ValueError(f"Matrices with incompatible shapes")

    def _matrix_operation(self, other: 'Matrix', op) -> 'Matrix':
        self._assert_dims(other)
        other_tr = zip(*other._data)
        new_data = [[sum(map(op, row, col)) for row in self._data] for col in other_tr]
        return Matrix(new_data)

    def __add__(self, other: 'Matrix') -> 'Matrix':
        return self._matrix_operation(other, add)

    def __mul__(self, other: 'Matrix') -> 'Matrix':
        self._assert_dims(other, is_total=True)
        new_data = [list(map(mul, row1, row2)) for (row1, row2) in zip(self._data, other._data)]
        return Matrix(new_data)

    def __matmul__(self, other: 'Matrix') -> 'Matrix':
        return self._matrix_operation(other, mul)
