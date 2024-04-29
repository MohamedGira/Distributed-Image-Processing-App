#run image_processing,py file for n threads. and poll
# Path: cleanCopy/components/execution/worker.py

import subprocess
import os
import sys
import pathlib
import logging
def wait_for_threads(threads):
    for i in range(len(threads)):
        threads[i].wait()
def kill_threads(threads):
    for i in range(len(threads)):
        threads[i].terminate()
    print("Interrupted")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
# get -worker arg from cmd


if __name__ == "__main__":
    workers= int(sys.argv[1]) if len(sys.argv)>1 else 5
    threads=[]
    try:
        logging.info("Starting worker threads")
        current_path = pathlib.Path(__file__).parent.absolute()
        for i in range(5):
            threads.append(subprocess.Popen(['python', current_path.joinpath("image_processing.py")], stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        logging.info("worker threads started")
        for i in range(5):
            threads[i].wait()
        logging.info("worker threads finished")

    except KeyboardInterrupt:
        kill_threads(threads)
        logging.error(print("Interrupted"))
        try:
            kill_threads(threads)
            sys.exit(0)
        except SystemExit:
            os._exit(0)
