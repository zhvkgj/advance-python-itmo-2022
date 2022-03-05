#!/usr/bin/python3

import numpy as np

from hw_3.src.matrix_common import AsListMixin, PersistentMixin, UtilityMixin


class Matrix(AsListMixin, PersistentMixin, UtilityMixin, np.lib.mixins.NDArrayOperatorsMixin):
    _HANDLED_TYPES = (np.ndarray,)

    def __init__(self, data: np.ndarray):
        self._data = data

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        for x in inputs:
            if not isinstance(x, self._HANDLED_TYPES + (Matrix,)):
                return NotImplemented
        inputs = tuple(x._data if isinstance(x, Matrix) else x
                       for x in inputs)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)
