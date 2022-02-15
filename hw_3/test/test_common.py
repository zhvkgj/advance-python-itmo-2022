#!/usr/bin/python3

import numpy as np


def generate_two_random_2d_ndarray():
    np.random.seed(0)
    return np.random.randint(0, 10, (10, 10)), np.random.randint(0, 10, (10, 10))


def run_test_common(directory: str, matrix1, matrix2):
    (matrix1 + matrix2).save_to_file(directory, '+')
    (matrix1 @ matrix2).save_to_file(directory, "@")
    (matrix1 * matrix2).save_to_file(directory, "*")
