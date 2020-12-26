import asyncio
import time


# 协程中是不能使用同步阻塞编程的
async def get_html(url):
    print('start get url', url)
    await asyncio.sleep(2)
    print('end get url')
    return 'get_futures'


# 函数必须要使用到future,就是完成好的函数
def call_back(future):
    time.sleep(8)
    print('tasks compete')


if __name__ == '__main__':
    start_time = time.time()
    # 事件循环,代替自己写的loop #获取主循环
    loop = asyncio.get_event_loop()

    # 1.使用future,获取future期望,传递给loop
    # get_future = asyncio.ensure_future(get_html('www.baidu.com'))
    get_future = loop.create_task(get_html('www.baidu.com'))
    # 把结果返回给callback函数
    get_future.add_done_callback(call_back)
    loop.run_until_complete(get_future)
    print('times', time.time() - start_time)
    print(get_future.result())