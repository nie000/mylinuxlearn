#模拟生产者消费者模型
import queue
import time

q = queue.Queue()



def product():
    con = consumer()
    next(con)
    num = 1
    while True:
        time.sleep(1)
        q.put(num)
        print('product num {}'.format(num))
        con.send('continue')
        num += 1

def consumer():
    while True:
        x = yield
        if x == "continue":
            res = q.get()
            time.sleep(10)
            print('consume num {}'.format(res))


product()