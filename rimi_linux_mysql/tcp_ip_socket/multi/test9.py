import time
import threading
import queue

tasks = queue.Queue()
# tasks = list()


# 生产者 消费者模型
# 布置任务的人  完成任务的人
# 布置的任务过快  完成的任务过慢

time.sleep(8)
time.sleep(4)
def teacher():
    num = 1
    while True:
        #每秒请求数量为 1000次 0.1秒布置一次任务
        time.sleep(1)
        tasks.put(num)
        print('布置了{}知识点'.format(num))
        num +=1


def student():
    while True:
        #每秒达到200次  -->在0.005秒之内完成这个任务
        time.sleep(5)
        num = tasks.get()
        print('终于学懂了{}知识点'.format(num))

executor = ThreadPoolExecutor(max_workers=2)

threading.Thread(target=teacher).start()
threading.Thread(target=student).start()
threading.Thread(target=student).start()
threading.Thread(target=student).start()
threading.Thread(target=student).start()
threading.Thread(target=student).start()
threading.Thread(target=student).start()
threading.Thread(target=student).start()
