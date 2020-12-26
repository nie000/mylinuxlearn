from concurrent.futures import ThreadPoolExecutor
import time
from functools import partial

# 1.并发
# 2.获取线程的返回值 当一个线程完成的时候,主线程能够知道
# 3.让多线程和多进程编程接口一致
def get_html(sleep_time,test):
    time.sleep(sleep_time)
    # print("get page {} success".format(sleep_time))
    return sleep_time

executor = ThreadPoolExecutor(max_workers=1)
# 通过sumbit提交到线程池中
task1 = executor.submit(partial(get_html,(2)),(2))
task2 = executor.submit(partial(get_html,(5)),(2))
task3 = executor.submit(partial(get_html,(5)),(2))

#必须取消没有执行的任务
# print(task3.cancel())
# done 用于判断是否完成

# 阻塞 等待任务完成获取结果

# 阻塞
res1 = task2.result()
res = task1.result()
print(task1.done())
# print(res)
# print(task2.result())
