#!/usr/bin/python3
from functools import lru_cache
from typing import List

from hw_3.src.matrix_easy import Matrix


class HashableMixin:
    """
    Mixin with dunder __hash__ which returns hash of this matrix.
    Hash is just a sum of values of matrix
    """

    def __hash__(self):
        return sum(map(sum, self._data))


class LRUCachedMatmulMatrix(Matrix, HashableMixin):
    def __init__(self, data: List[List[int]]):
        Matrix.__init__(self, data)

    @lru_cache(maxsize=128)
    def __matmul__(self, other: 'LRUCachedMatmulMatrix') -> 'LRUCachedMatmulMatrix':
        return LRUCachedMatmulMatrix(Matrix.__matmul__(self, other)._data)
