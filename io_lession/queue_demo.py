import time
import random
import queue
import threading


def product_task_to_queue(que):
    '''
    不断的像队列中去加入任务,每隔1，3秒加入一次
    :return:
    '''
    task_num = 1
    while True:
        print('product task', str(task_num),'task_size',que.qsize())
        que.put(str(task_num)) #如果达到最大值，会阻塞
        sleep_time = random.randint(1, 2)
        time.sleep(sleep_time)
        task_num += 1
def consume_task_from_queue(que):
    """
    不断的向队列中获取任务,然后消费任务,每隔2-4秒消费一次
    :param queue:
    :return:
    """
    while True:
        task_num = que.get()
        sleep_time = random.randint(3, 4)
        time.sleep(sleep_time)
        print('consume task num:', task_num, 'task_size', que.qsize())
def loop():
    que = queue.Queue(maxsize=10)
    t1 = threading.Thread(target=product_task_to_queue,args=(que,))
    t2 = threading.Thread(target=consume_task_from_queue, args=(que,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

loop()