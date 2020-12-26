from threading import Thread, RLock
import queue
import time
import random

tasks_num = 0
lock = RLock()


# 1. 放任务
# # 2. 取任务 并且 取完任务之后 任务就不在这个list里面了

def consumer(tasks):
    global lock
    while True:
        time.sleep(random.randint(5, 10))
        # get方法 如果list为空 那么会阻塞
        task = tasks.get()
        print('complete task num:{}'.format(task))
        print('left tasks num:{}'.format((tasks.qsize())))


def productor(tasks):
    global tasks_num
    while True:
        tasks_num += 1
        time.sleep(random.randint(1, 2))
        # 阻塞
        tasks.put(tasks_num)
        print('append new task num:{}'.format(tasks_num))


def main():
    tasks = queue.Queue(maxsize=3)
    t1 = Thread(target=productor, args=(tasks,))
    t2 = Thread(target=consumer, args=(tasks,))
    print('start project')
    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == "__main__":
    main()
