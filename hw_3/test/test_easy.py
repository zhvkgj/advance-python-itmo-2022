#!/usr/bin/python3
import hw_3.test.test_common as test_common
from hw_3.src.matrix_easy import Matrix


def run_easy_test():
    matrix1, matrix2 = test_common.generate_two_random_2d_ndarray()
    matrix1, matrix2 = Matrix(matrix1.tolist()), Matrix(matrix2.tolist())
    directory = "../artifacts/easy"
    test_common.run_test_common(directory, matrix1, matrix2)


if __name__ == '__main__':
    run_easy_test()
