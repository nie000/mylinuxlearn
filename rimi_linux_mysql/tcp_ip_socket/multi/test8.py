from concurrent.futures import ThreadPoolExecutor, as_completed, wait
import time
import random


def get_html(sleep_time):
    time.sleep(sleep_time)
    # print("get page {} success".format(sleep_time))
    return sleep_time


executor = ThreadPoolExecutor(max_workers=2)
# 通过sumbit提交到线程池中
tasks = list()
for i in range(10):
    sleep_time = random.randint(2, 5)
    tasks.append(executor.submit(get_html, (sleep_time)))

#阻塞等待任务完成
wait(tasks, return_when='FIRST_COMPLETED')
print('-----------')

#阻塞


for i in as_completed(tasks):
    data = i.result()

    print('num {} success'.format(data))

print('12312312')