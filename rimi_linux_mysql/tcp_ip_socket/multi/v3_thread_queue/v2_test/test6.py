from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
from functools import partial

def get_html(sleep_time,num):
    time.sleep(sleep_time)
    # print("get page {} success".format(sleep_time))
    return num


executor = ThreadPoolExecutor(max_workers=2)
# 通过sumbit提交到线程池中
tasks = list()
for i in range(10):
    sleep_time = random.randint(2, 5)
    #把右边函数看成一个整体
    tasks.append(executor.submit(partial(get_html,sleep_time), (i)))

#阻塞 等待完成的函数
for i in as_completed(tasks):
    data = i.result()

    print('num {} success'.format(data))