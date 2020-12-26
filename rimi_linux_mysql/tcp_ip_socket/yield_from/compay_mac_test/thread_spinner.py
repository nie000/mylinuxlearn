import threading
import itertools
import time
import sys

def spin(msg,signal):
    write,flush = sys.stdout.write,sys.stdout.flush

    for char in itertools.cycle('|/-\\'):
        status = char + " " + msg
        write(status)
        flush()
        write('\b' * len(status))
        time.sleep(0.1)





spin('adf',1)