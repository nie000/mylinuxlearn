#1.
#2.
#3.

import asyncio
import time
#协程中是不能使用同步阻塞编程的
async def get_html(url):
    print('start get url',url)
    await asyncio.sleep(2)
    print('end get url')

if __name__ == '__main__':
    start_time = time.time()
    #事件循环,代替自己写的loop
    loop = asyncio.get_event_loop()
    tasks = [get_html('www.baidu.com') for i in range(10)]
    loop.run_until_complete(asyncio.wait(tasks))
    print('times',time.time()-start_time)

