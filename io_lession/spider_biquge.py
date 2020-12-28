import requests
from lxml import etree

from mysql_helper import MysqlDB


class BasicSpider:
    max_repeat=None
    def get_url(self,url,data=None):
        try:
            r=requests.get(url,params=data,timeout=5)
            r.encoding='utf-8'
            rep=etree.HTML(r.text)
            return rep
        except Exception as e:
            print(e)
            if self.max_repeat>0:
                self.get_url(url,data)
                self.max_repeat-=1

class BiQuGeSpider(BasicSpider):
    max_repeat = 3
    def __init__(self):
        self.name='笔趣阁'
    def get_index_url(self):
        index_url='http://www.xbiquge.la/xiaoshuodaquan/'
        rep=self.get_url(index_url)
        url_list=rep.xpath('//*[@id="main"]/div[@class="novellist"]/ul/li/a/@href')
        return url_list
    def get_url_details(self,url_list):
        for url in url_list:
            data={}
            rep=self.get_url(url)
            data['url']=url
            data['name']=rep.xpath('//div[@id="info"]/h1/text()')[0]
            data['author']=rep.xpath('//div[@id="info"]/p[1]/text()')[0].replace('作\xa0\xa0\xa0\xa0者：','')
            data['create_time'] = rep.xpath('//div[@id="info"]/p[3]/text()')[0].replace('最后更新：','')
            self.save_data(data)
    def save_data(self,data):
        with MysqlDB() as cur:
            cur.execute('insert into biquge_data (`url`,`name`,`author`,`create_datetime`) values (%s,%s,%s,%s)',
                        [data['url'], data['name'], data['author'], data['create_time']])
if __name__ == '__main__':
    spider=BiQuGeSpider()
    url_list=spider.get_index_url()
    spider.get_url_details(url_list)