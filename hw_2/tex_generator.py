#!usr/bin/python3
import subprocess
import os
from functools import reduce
from typing import List

import click as click
from fibonacci_ast_visualizer import visualize


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


def table_and_image_to_tex(working_dir: str, table: List[List[str]]) -> str:
    def wrap_into_doc(content: str) -> str:
        return (f"\\documentclass{{article}}\n"
                f"\\usepackage{{graphicx}}\n"
                f"\\begin{{document}}\n\n"
                f"{content}\n\\end{{document}}")
    visualize.visualize_and_save(working_dir, "fib.jpg", False)
    return wrap_into_doc(table_to_tex(table) + image_to_tex(f"{working_dir}/fib.jpg"))


def save_to_file(directory: str, filename: str, content: str):
    with open(f"{directory}/{filename}", "w") as file:
        file.write(content)


def read_table_from_file(path_to_file: str) -> List[List[str]]:
    with open(path_to_file, "r") as file:
        return list(map(lambda line: line.split(), file))


def save_tex_as_pdf(tex_content: str, directory: str, filename: str):
    save_to_file(directory, filename, tex_content)
    subprocess.call(['pdflatex', '-output-directory', directory, filename])


@click.command()
@click.option("-i", default="table.txt", help="path to file with input table")
@click.option("-o", default="artifacts", help="directory for output")
@click.option("--name", default="table_with_image.pdf", help="name of a pdf file will be generated")
def generate_pdf(i: str, o: str, name: str):
    out = os.path.abspath(o)
    tex_content = table_and_image_to_tex(out, read_table_from_file(i))
    save_tex_as_pdf(tex_content, o, name)


if __name__ == '__main__':
    generate_pdf()
