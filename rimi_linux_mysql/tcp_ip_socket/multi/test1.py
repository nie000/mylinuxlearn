import time
import threading
import random
import queue

# 任务列表
lock = threading.RLock()


# 先进先出的队列
# [5,4,3,2,1]
# 生产者消费者模型
# 1. 两个线程 生产者线程 消费者线程
# 2. tasks 生产者向里面去放入数据 消费者取出数据

def product(tasks, i=0):

    while 1:

        i += 1
        task = 'task_id{}'.format(i)
        time.sleep(random.randint(1, 2))
        # 使用put向里面添加数据 如果队列满了 put就会阻塞
        print('product------')
        lock.acquire()
        tasks.append(task)
        lock.release()
        print('添加任务{}成功!'.format(i))




def consumer(tasks):
    while 1:
        time.sleep(random.randint(5, 8))
        # tasks 是空的时候
        # 遇到pop阻塞
        # 使用Get去数据 如果没有数据的话 阻塞
        task = tasks.get()
        print('完成任务编号: {} 成功!'.format(task))


# GIL   LOCK

if __name__ == '__main__':
    # 1.先进先出
    # 2.自带锁 操作的这个queue的时候,不用考虑gil
    # 3.当你去的数据的时候,如果没有数据,会阻塞
    # 4.可以规定队列的大小
    tasks = []
    # 阻塞 单线程
    i = 0
    # 子线程1
    t1 = threading.Thread(target=product, args=(tasks, i))
    t2 = threading.Thread(target=consumer, args=(tasks,))
    t1.start()
    t2.start()
    # join 阻塞主线程

    print('任务执行完毕')
