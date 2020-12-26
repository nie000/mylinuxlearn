from concurrent.futures import ThreadPoolExecutor
import time
import threading
from functools import partial

def consume(num,test):
    print(test)
    time.sleep(10)
    print('consuming',num)
#pools代表的是线程池
pools = ThreadPoolExecutor(10)

num = 1
i = 1
while True:
    time.sleep(0.1)
    #偏函数 需要你传递引用的时候,引用无法带参数,
    pools.submit(partial(consume,(num,7)))
    print('sumbit',i)
    # threading.Thread(target=consume,args=(num,)).start()
    i +=1
    num += 1
