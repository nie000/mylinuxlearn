from random import randint
from time import sleep
from queue import Queue
from v2_class_usage import TestThread


def writeQ(queue):
    print('producing object for Q')
    queue.put('xxx', 1)
    print('size now', queue.qsize())


def readQ(queue):
    val = queue.get(1)
    print('consumed object from Q... size now', queue.qsize())


def writer(queue, loops):
    for i in range(loops):
        writeQ(queue)
        sleep(randint(1, 2))


def reader(queue, loops):
    for i in range(loops):
        readQ(queue)
        sleep(randint(5, 13))


funcs = [writer, reader]

nfuncs = range(len(funcs))


def main():
    nloops = randint(2, 5)
    q = Queue(32)
    threads = list()
    for i in nfuncs:
        t = TestThread(funcs[i], (q, nloops))

        threads.append(t)

    for i in threads:
        i.start()

    for i in threads:
        i.join()

    print("all down")


if __name__ == '__main__':
    main()
