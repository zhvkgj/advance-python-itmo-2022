#!/usr/bin/python3
import pathlib
import time

from fibonacci import fibonacci as fib

from threading import Thread
import multiprocessing as mp

import click


def timeit(method):
    def timed(*args, **kw):
        ts = time.monotonic()
        method(*args)
        te = time.monotonic()

        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = te - ts
    return timed


class FibBenchmark:
    def __init__(self, n: int):
        self.n = n
        self.logtime_data = None
        self.threads = [Thread(target=fib, args=(self.n, )) for _ in range(10)]
        self.processes = [mp.Process(target=fib, args=(self.n, )) for _ in range(10)]

    @timeit
    def run_with_single_thread(self):
        for _ in range(10):
            fib(self.n)

    @timeit
    def run_with_ten_threads(self):
        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()

    @timeit
    def run_with_ten_processes(self):
        for process in self.processes:
            process.start()

        for process in self.processes:
            process.join()

    def run(self):
        self.logtime_data = dict()
        self.run_with_single_thread(log_time=self.logtime_data)
        self.run_with_ten_threads(log_time=self.logtime_data)
        self.run_with_ten_processes(log_time=self.logtime_data)

    def save_to_file(self, filename: str):
        proj_dir = pathlib.Path(__file__).parent.parent.resolve()
        with open(f"{proj_dir}/artifacts/{filename}.txt", "w") as file:
            file.write("Benchmark results:\n")
            file.writelines(f"\tfor {name} time is: {t:0.8f} sec\n"
                            for name, t in self.logtime_data.items())


@click.command()
@click.option('--num', default=50, help='Fibonacci number')
def cli(num: int):
    bench = FibBenchmark(num)
    bench.run()
    bench.save_to_file("fib_benchmark_result")


if __name__ == "__main__":
    cli()
