# 两个队列,一个生产者不断的去队列里面存放任务,一个消费者,不断的取队列里面消费任务
import time
import random
import queue
import threading


def product_task_to_queue(queue):
    '''
    不断的像队列中去加入任务,每隔1，3秒加入一次
    :return:
    '''
    task_num = 1
    while True:
        print('product task', str(task_num),'task_size',queue.qsize())
        queue.put(str(task_num))
        sleep_time = random.randint(1, 2)
        time.sleep(sleep_time)
        task_num += 1


def consume_task_from_queue(queue):
    """
    不断的向队列中获取任务,然后消费任务,每隔2-4秒消费一次
    :param queue:
    :return:
    """
    while True:
        task_num = queue.get()
        sleep_time = random.randint(3, 4)
        time.sleep(sleep_time)
        consume_task(task_num,queue)


def consume_task(task_num,queue):
    """
    消费任务的函数
    :param task_num:
    :return:
    """
    print('consume task num:', task_num,'task_size',queue.qsize())


def loop():
    que = queue.Queue(maxsize=10)
    t1 = threading.Thread(target=product_task_to_queue,args=(que,))
    t2 = threading.Thread(target=consume_task_from_queue, args=(que,))


    t1.start()
    t2.start()
    t1.join()
    t2.join()

loop()