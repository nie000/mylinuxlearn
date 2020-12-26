from concurrent.futures import ThreadPoolExecutor
import time

#简单的线程池使用
def consume(num):
    time.sleep(4)
    print('consuming',num)

pools = ThreadPoolExecutor(3)

num = 1
while True:

    time.sleep(1)
    pools.submit(consume,(num))
    num += 1
