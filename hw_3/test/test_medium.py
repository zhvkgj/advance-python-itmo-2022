#!/usr/bin/python3

import hw_3.test.test_common as test_common
from hw_3.src.matrix_medium import Matrix


def run_medium_test():
    matrix1, matrix2 = test_common.generate_two_random_2d_ndarray()
    matrix1, matrix2 = Matrix(matrix1), Matrix(matrix2)
    directory = "../artifacts/medium"
    test_common.run_test_common(directory, matrix1, matrix2)


if __name__ == '__main__':
    run_medium_test()
