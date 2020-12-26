import threading
import queue
import time
import random

tasks = queue.Queue()

def pro():
    global tasks

    while 1:
        time.sleep(1)
        num = random.randint(0,1000000)
        tasks.put(num)
        print('布置了一个任务{}'.format(num))


def con():
    global tasks
    while 1:
        time.sleep(2)
        num = tasks.get()
        print('完成了 {} 任务'.format(num))
        print('当前任务剩余 {} 个'.format(tasks.qsize()))


def main():
    t1 = threading.Thread(target=pro)
    t2 = threading.Thread(target=con)

    t1.start()
    t2.start()

    t1.join(
    )
    t2.join()

if __name__ == "__main__":
    main()


