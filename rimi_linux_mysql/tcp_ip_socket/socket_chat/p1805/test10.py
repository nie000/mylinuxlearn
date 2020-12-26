# 期货
from concurrent.futures import ThreadPoolExecutor,as_completed
from threading import Thread
#偏函数
# from functools import partial
import time
import random
def get_html(num,res):
    time.sleep(num)
    return res
ex = ThreadPoolExecutor(max_workers=10)
# Thread(target=get_html,args=(5,'task1')).start()
task1 = ex.submit(get_html,10,'task1')
#futures 类
task2 = ex.submit(get_html,1,'task2')
tasks = list()
for i in range(1,11):
    tasks.append(ex.submit(get_html,random.randint(1,10),'task{}'.format(str(i))))
#
#
for i in as_completed(tasks):
    print(i.result())


