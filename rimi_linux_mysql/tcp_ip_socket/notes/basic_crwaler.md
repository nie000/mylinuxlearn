# 简单爬虫基础

## 概述

1. 网络爬虫（又被称为网页蜘蛛，网络机器人，在FOAF社区中间，更经常的称为网页追逐者），是一种按照一定的规则，自动地抓取万维网信息的程序或者脚本。另外一些不常使用的名字还有蚂蚁、自动索引、模拟程序或者蠕虫。

2. 爬虫的基本步骤是 

    1. 找到网站的入口
    2. 解析网站的html提取信息
    3. html中有许多不同的a连接,使用同样的方式,进入连接中去爬去不同的网页代码


3. 爬虫需要用到的工具

    1. 我们需要一个url解析的工具
    2. 需要一个请求html网页的工具 
    3. 需要一个解析html代码的工具

    
## 软件安装

1. requests库 用于请求网页
	```
	pip install requests
	```


2. bs4库 用于解析html 类似于dom

    ``` 
    pip install beautifulsoup4
    pip install lxml
    ```    
    
## 爬虫示例

1. 软件的示例

	> tcp_ip_socket/crwaler/basic_crwaler/test1.py
	
    ``` 
    import requests
	from bs4 import BeautifulSoup
	
	
	def get_html_doc(url):
	    # 根据指定的url获取html文档
	    res = requests.get(url)
	    return res.content.decode("utf8")
	
	
	if __name__ == "__main__":
	    url = "http://www.jobbole.com/"
	    a = get_html_doc(url)
	    data = BeautifulSoup(a)
	
	    pass

    ```
    
    1. 我们把url交给request去请求html文档
    2. 把html文档传递给 BeautifulSoup去加载
    3. data就有了类似于js dom树的功能
    
2. 复杂的爬虫

    我们需要遍历所有的文章,经过观察,我们发现,伯乐在线有一个index的页面,页面中展示每篇文章的标题和概述,点击进去才有详细的文章。我们可以通过爬去index页面,获取详细页面的url。再爬去详细页面的url，这样去爬取整个网站的文章
    
    1. 实验第一步,爬去文章列表页,然后把列表页的url提取出来,再爬去详细文章页面
    
    >tcp_ip_socket/crwaler/basic_crwaler/test1.py
    
    
    
    ```
    
    import requests
	from bs4 import BeautifulSoup
	
	
	def get_html_doc(url):
	    # 根据指定的url获取html文档
	    res = requests.get(url)
	    # print(res.content)
	    return res.content.decode("utf8")
	
	
	if __name__ == "__main__":
	    url = "http://blog.jobbole.com/category/it-tech/"
	    a = get_html_doc(url)
	    data = BeautifulSoup(a)
	    #把index里面的url取出来再取下面的url
	    #data.select调用css选择器 选择出来是dict
	    urls =data.select('[class=post-thumb] a')
	
	    for i in urls:
	        url = i['href']
	        get_html_doc(url)
    
    ```    
3. 根据列表页面中的url无限获取

	1. 指定一个入口url
	2. 通过入口url获取index页面
	3. 通过index的url解析子页面
	4. 通过index中的其他跳转页面获取其他index页面

    ```
    
    import requests
	from bs4 import BeautifulSoup
	
	index_urls_list = []
	
	
	def get_html_doc(url):
	    # 根据指定的url获取html文档
	    res = requests.get(url)
	    print(res.content)
	    return res.content.decode("utf8")
	
	
	def parse_index(url):
	    # 解析列表页面
	    html_doc = get_html_doc(url)
	    data = BeautifulSoup(html_doc)
	    # 把index里面的url取出来再取下面的url
	    # data.select调用css选择器 选择出来是dict
	    detail_urls = data.select('[class=post-thumb] a')
	
	    for i in detail_urls:
	        url = i['href']
	        get_html_doc(url)
	    # 取出所有其他index页面的翻页url 去解析其他的url
	    index_urls = data.select('a[class=page-numbers]')
	    for i in index_urls:
	        if i not in index_urls_list:
	            index_urls_list.append(i)
	            url = i['href']
	            parse_index(url)
	
	
	def start(url):
	    parse_index(url)
	
	
	if __name__ == "__main__":
	    url = "http://blog.jobbole.com/category/it-tech/"
	    start(url)

    
    ```
