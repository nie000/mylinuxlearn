from concurrent.futures import ThreadPoolExecutor,as_completed
import time
# 1.并发
# 2.获取线程的返回值 当一个线程完成的时候,主线程能够知道
# 3.让多线程和多进程编程接口一致
def get_html(sleep_time):
    time.sleep(sleep_time)
    print("get page {} success".format(sleep_time))
    return sleep_time


executor = ThreadPoolExecutor(max_workers=2)
#通过sumbit提交到线程池中
task1 = executor.submit(get_html,(3))
task2 = executor.submit(get_html,(2))
task3 = executor.submit(get_html,(2))

print(task3.cancel())
# done 用于判断是否完成
# print(task1.done())
# 阻塞 等待任务完成获取结果
print(task1.result())
print(task2.result())
