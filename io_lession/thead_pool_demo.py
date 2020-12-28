# from concurrent.futures import ThreadPoolExecutor
# import time
#
# #简单的线程池使用
# def consume(a):
#     time.sleep(10)
#     print('consuming',a)
#
# pools = ThreadPoolExecutor(3)
#
# num = 1
# while True:
#
#     time.sleep(0.5)
#     pools.submit(consume,(num))
#     num += 1
#     print(num)


# from concurrent.futures import ThreadPoolExecutor
# import time
# # 1.并发
# # 2.获取线程的返回值 当一个线程完成的时候,主线程能够知道
# # 3.让多线程和多进程编程接口一致
# def get_html(sleep_time):
#     time.sleep(sleep_time)
#     print("get page {} success".format(sleep_time))
#     return sleep_time
#
#
# executor = ThreadPoolExecutor(max_workers=2)
# #通过sumbit提交到线程池中
# task1 = executor.submit(get_html,(3))
# task2 = executor.submit(get_html,(2))
# task3 = executor.submit(get_html,(2))
#
# # print(task3.cancel())
#
#
# # done 用于判断是否完成
# print(task1.done())
# print('22222222')
# # 阻塞 等待任务完成获取结果
# print(task1.result())
# print(task2.result())
# print('爬虫爬取完成！')



from concurrent.futures import ThreadPoolExecutor, as_completed, wait
import time
import random
from functools import partial

def get_html(sleep_time,num):
    time.sleep(sleep_time)
    print("num {},get page {} success".format(num,sleep_time))
    return num


executor = ThreadPoolExecutor(max_workers=2)
# 通过sumbit提交到线程池中
tasks = []
for i in range(10):
    sleep_time = random.randint(2, 5)
    #把右边函数看成一个整体
    tasks.append(executor.submit(get_html, sleep_time,i))

wait(tasks, return_when='ALL_COMPLETED')
print('111111')
#阻塞 等待完成的函数
for i in as_completed(tasks):
    data = i.result()

    print('num {} success'.format(data))