#!/usr/bin/python3

import concurrent.futures as cn
import logging
import math
import multiprocessing as mp
import pathlib
import time
from functools import reduce
from itertools import zip_longest


def timeit(method):
    def timed(*args, **kw):
        ts = time.monotonic()
        m_kw = {i: kw[i] for i in kw if i != 'log_time'}
        method(*args, **m_kw)
        te = time.monotonic()

        if 'log_time' in kw:
            kw['log_time'].append(te - ts)

    return timed


proj_dir = pathlib.Path(__file__).parent.parent.resolve()

logging.basicConfig(filename=f"{proj_dir}/artifacts/integrate.log",
                    filemode="w",
                    level=logging.INFO,
                    format="%(name)s - %(levelname)s - %(message)s")


def save_to_file(timings, th_timings, mp_timings):
    with open(f"{proj_dir}/artifacts/time_comparison.txt", "w") as file:
        file.write("Benchmark results:\n")
        file.writelines(f"\tfor {i + 1} jobs time is: {ts:0.8f} sec (single thread), "
                        f"{tt:0.8f} sec (multithreading), {tp:0.8f} sec (multiprocessing)\n"
                        for i, (ts, tt, tp) in enumerate(zip_longest(timings, th_timings, mp_timings)))


def processing(f, chunk, step, n_job) -> int:
    logging.info(f"Job with number {n_job} started...")
    return sum(map(lambda x: f(x) * step, chunk))


@timeit
def integrate_concurrent(f, a, b, *, n_jobs=1, n_iter=1000, pool: cn.Executor):
    step = (b - a) / n_iter
    iterable = [a + i * step for i in range(n_iter)]
    chunksize = (n_iter + n_jobs - 1) // n_jobs
    futures = [pool.submit(processing, f,
                           iterable[job * chunksize:(job + 1) * chunksize],
                           step, job)
               for job in range(n_jobs)]
    return reduce(lambda x, future: x + future.result(), futures, 0)


def integrate_with_thread_pool(f, a, b, *, n_jobs=1, n_iter=1000, logtime):
    logging.info(f"Multithreading integrate activity with {n_jobs} jobs started...\n")
    with cn.ThreadPoolExecutor(max_workers=n_jobs) as executor:
        return integrate_concurrent(f, a, b, n_jobs=n_jobs, n_iter=n_iter, pool=executor, log_time=logtime)


def integrate_with_process_pool(f, a, b, *, n_jobs=1, n_iter=1000, logtime):
    logging.info(f"Multiprocessing integrate activity with {n_jobs} jobs  started...\n")
    with cn.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        return integrate_concurrent(f, a, b, n_jobs=n_jobs, n_iter=n_iter, pool=executor, log_time=logtime)


@timeit
def integrate(f, a, b, *, n_jobs=1, n_iter=1000):
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def main():
    f = math.cos
    a = 0
    b = math.pi / 2
    ts = []
    tt = []
    tp = []
    for i in range(1, mp.cpu_count() * 2 + 1):
        integrate(f, a, b, n_jobs=i, log_time=ts)
        integrate_with_thread_pool(f, a, b, n_jobs=i, logtime=tt)
        integrate_with_process_pool(f, a, b, n_jobs=i, logtime=tp)
    save_to_file(ts, tt, tp)


if __name__ == '__main__':
    main()
