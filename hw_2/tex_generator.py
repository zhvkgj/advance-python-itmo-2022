#!usr/bin/python3
import subprocess
import os
from functools import reduce
from typing import List
from fibonacci_ast_visualizer import visualize


def save_to_file(directory: str, filename: str, content: str):
    with open(f"{directory}/{filename}", "w") as file:
        file.write(content)


def assert_dim(table: List[List[str]]):
    incorrect = True
    if table:
        cols = len(table[0])
        for row in table:
            if len(row) != cols:
                break
        else:
            incorrect = False

    if incorrect:
        raise ValueError("malformed table")


def table_to_tex(table: List[List[str]]) -> str:
    def concat_with(ls, delim='\\\\') -> str:
        return reduce(lambda a, b: f"{a}{delim}{b}", ls)

    def add_header(rest: str) -> str:
        return (f"\\begin{{center}}\n"
                f"\t\\begin{{tabular}}"
                f"{{{concat_with(map(lambda _: 'c', table), '|')}}}\n"
                f"\t\t\\hline\n"
                f"{rest}")

    def add_footer(first: str) -> str:
        return (f"{first}"
                f"\n\t\\end{{tabular}}\n"
                f"\\end{{center}}\n")

    def convert_row(row: List[str]) -> str:
        def break_elem(elem: str) -> str:
            return f"\\parbox[c]{{3cm}}{{{concat_with([elem[i:i + 16] for i in range(0, len(elem), 16)])}}}"

        return f"\t\t{concat_with(map(break_elem, row), ' & ')} \\\\ \\hline"

    assert_dim(table)
    return add_footer(add_header(concat_with(map(convert_row, table), '\n')))


def image_to_tex(path_to_image: str) -> str:
    return f"\\includegraphics[scale=0.2]{{{path_to_image}}}\n"


def pdf_with_table_and_image(directory: str, filename: str, table: List[List[str]]):
    def wrap_into_doc(content: str):
        return (f"\\documentclass{{article}}\n"
                f"\\usepackage{{graphicx}}\n"
                f"\\begin{{document}}\n\n"
                f"{content}\n\\end{{document}}")
    abspath = os.path.abspath(directory)
    image_name = "fib.jpg"
    visualize.visualize_and_save(abspath, image_name, False)
    image_tex = image_to_tex(f"{abspath}/{image_name}")
    table_tex = table_to_tex(table)
    save_to_file(abspath, filename, wrap_into_doc(table_tex + image_tex))
    subprocess.call(['pdflatex', '-output-directory', abspath, filename])


if __name__ == '__main__':
    example_table = [
        ['1111111111111111', '222222222222222', '3'],
        ['4444444444444444444', '5', '666666'],
        ['7', '8888888', '99']
    ]
    pdf_with_table_and_image("artifacts", "table-image.tex", example_table)
