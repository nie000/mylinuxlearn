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
    pass
