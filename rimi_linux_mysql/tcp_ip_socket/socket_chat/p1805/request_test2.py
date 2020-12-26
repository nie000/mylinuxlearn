import requests
from bs4 import BeautifulSoup
from threading import  Thread

r = requests.get('http://blog.jobbole.com/114499/')
html = r.text
dom = BeautifulSoup(html)
a_list = dom.find_all('span',class_='digg-item-updated-title')
x = a_list[0].find('a')
href = x.attrs.get('href',None)
x = 1

#获取html
def get_html(url):
    r = requests.get(url)
    html = r.text
    # logs(html)
    Thread(target=get_html,args=(url,))
    return html

def parse_a(html):
    dom = BeautifulSoup(html)
    a_list = dom.find_all('span', class_='digg-item-updated-title')

    all_list = []
    for i in a_list:
        a = i.find('a')
        href = a.attrs.get('href', None)
        if href:
            all_list.append(href)

    return all_list

def logs(html):
    print(html)


def start(url="http://python.jobbole.com/89290/"):
    html = get_html(url)
    a_list = parse_a(html)
    for i in a_list:
        start(i)

if __name__ == "__main__":
    start()






