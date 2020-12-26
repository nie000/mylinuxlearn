# 1. 早上的socket

# 2. 爬取index页面 通过 http://blog.jobbole.com/all-posts/  把1-500页都爬出来
    # 1. 递归方式爬取
    # 2. 生成者消费者模型爬
    # 3. 两个方式的不同

# 3. 通过2把详情页面的a标签爬出来,放到一个任务里面, 另外一个函数取a标签,并且爬取a标签的页面

from bs4 import BeautifulSoup
import threading
import requests
#已经被爬取的页面
crawled_index_list = []
crawled_num = 0

# 1000次 1.3
def get_index(url):
    global crawled_index_list
    global crawled_num
    if url in crawled_index_list:
        return False
    html = requests.get(url=url)
    crawled_num += 1
    print(crawled_num)
    crawled_index_list.append(url)
    # print(html.text)
    if url == "http://python.jobbole.com/all-posts/page/84/":
        return html
    #为什么js控制html
    #对象
    dom = BeautifulSoup(html.text)
    a_tag_lists = dom.find_all('a', class_='next page-numbers')
    for i in a_tag_lists:
        href = i.attrs['href']
        threading.Thread(target=get_index,args=(href,)).start()



get_index('http://blog.jobbole.com/all-posts/')
