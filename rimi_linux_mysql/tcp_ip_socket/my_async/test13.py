import asyncio
import time

# 协程中是不能使用同步阻塞编程的
async def get_html(url):
    print('start get url1', url)
    await asyncio.sleep(2)
    print('end get url1')

async def get_html2(url):
    print('start get url2', url)
    await asyncio.sleep(7)
    print('end get url2')

if __name__ == '__main__':
    start_time = time.time()
    # 事件循环,代替自己写的loop
    loop = asyncio.get_event_loop()
    t1 = [get_html('www.baidu.com') for i in range(10)]
    t2 = [get_html2('www.google.com') for i in range(10)]
    tasks = asyncio.gather(*t1)
    tasks2 = asyncio.gather(*t2)
    try:
        loop.run_until_complete(asyncio.gather(tasks, tasks2))
    except KeyboardInterrupt:
        print(tasks2.cancel())
        loop.stop()

    print('times', time.time() - start_time)