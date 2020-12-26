import aiohttp
import asyncio
import requests
#协程 可以暂停函数
from asyncio.queues import Queue
from queue import Queue


def get():
    requests.get('asdf')

async def fetch(session,url):
    async with session.get(url) as response:
        #可能是多线程 可能是 Io多路
        html = await response.text()
        return html
async def main(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session,url)
        print(html)
loop = asyncio.get_event_loop()
loop.run_until_complete(main('http://www.jobbole.com'))

