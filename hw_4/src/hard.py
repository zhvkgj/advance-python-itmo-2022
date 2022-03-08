#!/usr/bin/python3
import codecs
import logging
import multiprocessing as mp
from multiprocessing import connection
import pathlib
import threading
import time
from sys import stdin

proj_dir = pathlib.Path(__file__).parent.parent.resolve()

logging.basicConfig(filename=f"{proj_dir}/artifacts/hard.log",
                    filemode="w",
                    level=logging.INFO,
                    format="%(asctime)s %(name)s - %(levelname)s - %(message)s")


def rot13_routine(in_a_conn: connection.Connection, in_b_conn: connection.Connection,
                  out_a_conn: connection.Connection, out_b_conn: connection.Connection):
    in_b_conn.close()
    out_a_conn.close()
    try:
        while True:
            message = in_a_conn.recv()
            encoded = codecs.encode(message, 'rot_13')
            out_b_conn.send(encoded)
    except EOFError:
        pass


def lower_routine(queue: mp.Queue, in_conn: connection.Connection, out_conn: connection.Connection):
    in_conn.close()
    try:
        while True:
            message = queue.get()
            if message == "DONE":
                break
            out_conn.send(message.lower())
            time.sleep(5)
    except EOFError:
        pass


def print_zot13(in_conn: connection.Connection):
    try:
        while True:
            message = in_conn.recv()
            logging.info(f"output: {message}")
            print(message)
    except EOFError:
        pass


def main_process_routine(queue: mp.Queue):
    for line in stdin:
        logging.info(f"input: {line}")
        queue.put(line)
    queue.put("DONE")


def main():
    queue = mp.Queue()
    in_a, out_a = mp.Pipe(duplex=False)
    in_b, out_b = mp.Pipe(duplex=False)

    a = mp.Process(target=lower_routine, args=(queue, in_a, out_a,))
    b = mp.Process(target=rot13_routine, args=(in_a, out_a, in_b, out_b,))
    thread = threading.Thread(target=print_zot13, args=(in_b, ))

    a.start()
    b.start()
    thread.start()
    main_process_routine(queue)

    queue.close()
    in_a.close()
    out_a.close()
    in_b.close()
    out_b.close()

    thread.join()
    a.join()
    b.join()


if __name__ == "__main__":
    main()
