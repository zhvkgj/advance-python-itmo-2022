#!/usr/bin/python3
import pathlib
from typing import Tuple


class AsListMixin:
    """
    Mixin with shape and list properties that returns
    sizes along the dimensions and
    list view on this matrix accordingly
    """

    @property
    def shape(self) -> Tuple[int, int]:
        if not self._data:
            raise ValueError("Non initialized")

        return len(self._data), len(self._data[0])

    @property
    def list(self):
        return self._data


class PersistentMixin:
    """
    Mixin with method save_to_file which writes this matrix to a specified file
    """

    def save_to_file(self, directory: str, suffix: str):
        proj_dir = pathlib.Path(__file__).parent.resolve()
        with open(f"{proj_dir}/{directory}/matrix{suffix}.txt", "w") as file:
            file.writelines('\t'.join(str(el) for el in row) + '\n' for row in self._data)


class UtilityMixin:
    """
    Mixin with utility methods such as:
        str -- returns string representation of this matrix object
        repr -- returns straightforward information about this matrix object
    """
    def __str__(self):
        # idk what should I write here
        return self.__repr__()

    def __repr__(self):
        return f"{self.__class__.__name__}(data={self._data})"


class HashableMixin:
    """
    Mixin with dunder __hash__ which returns hash of this matrix.
    Hash is evaluated by the formula:
    """
    def __hash__(self):
        pass
