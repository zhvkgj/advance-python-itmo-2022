#!/usr/bin/python3
from hw_3.src.matrix_hard import LRUCachedMatmulMatrix


def run_hard_test():
    matrix_a, matrix_c = LRUCachedMatmulMatrix([[5, 6], [7, 8]]), LRUCachedMatmulMatrix([[7, 8], [5, 6]])
    matrix_b = LRUCachedMatmulMatrix([[1, 2], [3, 4]])
    matrix_d = matrix_b

    directory = "../artifacts/hard"
    matrix_a.save_to_file(directory, "_A")
    matrix_b.save_to_file(directory, "_B")
    matrix_c.save_to_file(directory, "_C")
    matrix_d.save_to_file(directory, "_D")
    matrix_ab = matrix_a @ matrix_b
    matrix_ab.save_to_file(directory, "_AB")
    matrix_cd = matrix_c @ matrix_d
    matrix_cd.save_to_file(directory, "_CD")
    hash_ab = hash(matrix_ab)
    hash_cd = hash(matrix_cd)
    LRUCachedMatmulMatrix([[hash_ab, hash_cd]]).save_to_file(directory, "_hash")


if __name__ == '__main__':
    run_hard_test()
