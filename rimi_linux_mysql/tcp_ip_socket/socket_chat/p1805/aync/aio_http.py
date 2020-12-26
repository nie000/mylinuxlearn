# 官网 https://aiohttp.readthedocs.io/en/stable/
import aiohttp
import asyncio
from bs4 import BeautifulSoup

index_q = asyncio.Queue()
detail_q = asyncio.Queue()

num = 0


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            global num
            num += 1
            print(num)
            # print(html)
            return html


async def run_index():
    await index_q.put("http://blog.jobbole.com/all-posts/")
    while 1:
        url = await index_q.get()
        # print('index_url',url)
        # html = await fetch(url)

        html = await asyncio.ensure_future(fetch(url))
        await parse_index(html)


async def run_detail():
    global loop
    while 1:
        url = await detail_q.get()
        # print('detail_url',url)

        asyncio.ensure_future(fetch(url))

        # task = loop.create_task(fetch(url))
        # await asyncio.wait(task)
        html = await fetch(url)


async def parse_index(html):
    # print('parse')
    try:
        url_all = BeautifulSoup(html)

        # # 布置Index页面的任务
        next_urls = url_all.find_all("a", attrs={"class": 'next page-numbers'})
        for i in next_urls:
            next_url = i.get('href')
            await index_q.put(next_url)
            # task = asyncio.ensure_future(run_index(next_url))
            # tasks.append(task)
            #
            # await asyncio.gather(task)


        # 布置详情页面的任务
        a_list = url_all.find_all('a', class_='archive-title')
        # map(lambda x: await detail_q.put(x.get('href')), a_list)
        for i in a_list:
            href = i.get('href')
            await detail_q.put(href)
        #     task = asyncio.ensure_future(fetch(href))
        #     tasks.append(task)
        # await asyncio.gather(*tasks)
            # [detail_q.put_nowait(url.get('href')) for url in a_list]
    except Exception:
        pass


# asyncio 高并发库
# def tasks():
#     task = list()
#     for i in range(114499, 125499):
#         # 114499 http://blog.jobbole.com/114499/
#         task.append(star())
#     return task


loop = asyncio.get_event_loop()
tasks = [run_index(),run_detail()]
loop.run_until_complete(asyncio.wait(tasks))


a = [x for x in range(1000)]

b = list()
for i in range(1000):
    b.append(i)