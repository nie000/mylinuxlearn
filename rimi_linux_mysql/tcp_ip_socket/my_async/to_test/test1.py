from tornado import httpclient, ioloop,queues
from functools import partial
from bs4 import BeautifulSoup


async def get_html(url):
    res = await httpclient.AsyncHTTPClient().fetch(url)
    html = res.body.decode('utf8')
    return html

async def get_index(url):
    pass

async def start_url(url):
    q = queues.Queue()
    start_html = await get_html(url)
    data = BeautifulSoup(start_html)
    detail_urls = data.select('[class=post-thumb] a')

    print(detail_urls)
    for i in detail_urls:
        url = i['href']
        # print('productor------>', url)
        q.put(url)

    async for i in q:
        res = await get_html(i)
        r = BeautifulSoup(res)
        print(r.title.string)

    # 取出所有其他index页面的翻页url 去解析其他的url
    # index_urls = data.select('a[class=page-numbers]')
    # for i in index_urls:
    #     url = i['href']
    #     index_urls_queue.put(url)
    #     # 去重 使用redis数据库
    #     print('put_index_url--->', url)


async def main(url):
    res = await get_html(url)
    print(res)


if __name__ == '__main__':
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(partial(start_url, 'http://blog.jobbole.com/all-posts/'))
