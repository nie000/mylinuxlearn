#生成者消费者模型

import queue
import time
import random
import threading
tasks = queue.Queue()


def product():
    while 1:
        time.sleep(1)
        num = random.randint(0,3000000)
        tasks.put(num)
        print('产生了一个任务{}'.format(num))
        print('当前任务数量:{}'.format(tasks.qsize()))
        print('-------------------')


def consumer():
    while 1:
        time.sleep(2)
        num = tasks.get()
        print('消费了任务{}'.format(num))
        print('当前任务数量:{}'.format(tasks.qsize()))


threading.Thread(target=product).start()
threading.Thread(target=consumer).start()