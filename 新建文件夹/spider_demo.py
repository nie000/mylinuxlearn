import requests

# url='http://www.xbiquge.la/11/11621/'
# response=requests.get(url)
# response.encoding='utf-8'
# print(response.text)

# url='http://www.baidu.com'
# r=requests.get(url,params={'wd':'韩富强'},headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'})
# r.encoding='utf-8'
# print(r.text)
# print('网页编码是',r.encoding) #打印默认值，如果人为定义了则打印的是你设
# print('请求的 url 是',r.url)
# print('响应头',r.headers)
# print('相应状态码',r.status_code)
# print('请求历史',r.history)
# print('是否重定向',r.is_redirect)
# # print('二进制内容',r.content)

#cookie保持登录状态
# url='http://www.xbiquge.la/modules/article/bookcase.php'
# # r=requests.get(url,cookies={'_abcde_qweasd':'0','BAIDU_SSP_lcr':'https://www.baidu.com/link?url=wtWviN2JHpsnCJt44m_bjr5DKhsLNhyQd4fN4h0hu7W&wd=&eqid=e53ef0bd000b5dd1000000065de604ca'})
# url_header={
#     'Cookie': '_abcde_qweasd=0; BAIDU_SSP_lcr=https://www.baidu.com/link?url=wtWviN2JHpsnCJt44m_bjr5DKhsLNhyQd4fN4h0hu7W&wd=&eqid=e53ef0bd000b5dd1000000065de604ca; _abcde_qweasd=0; Hm_lvt_169609146ffe5972484b0957bd1b46d6=1575355627; bdshare_firstime=1575355626663; PHPSESSID=1ffpqt37bjvp2h2rmu8pfnrt10; username=zhangke; Hm_lpvt_169609146ffe5972484b0957bd1b46d6=1575358190',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
# }
# r=requests.get(url,headers=url_header)
# r.encoding='utf-8'
# print(r.text)

# #post实现自动登录
# url='http://www.xbiquge.la/login.php?jumpurl=http://www.xbiquge.la/'
# url_header={
# 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
# 'Accept-Encoding': 'gzip, deflate',
# 'Accept-Language': 'zh-CN,zh;q=0.9',
# 'Cache-Control': 'max-age=0',
# 'Connection': 'keep-alive',
# 'Content-Length': '62',
# 'Content-Type': 'application/x-www-form-urlencoded',
# 'Host': 'www.xbiquge.la',
# 'Origin': 'http://www.xbiquge.la',
# 'Referer': 'http://www.xbiquge.la/',
# 'Upgrade-Insecure-Requests': '1',
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
# }
# r=requests.post(url,data={'LoginForm[username]':'zhangke','LoginForm[password]':'123123'},allow_redirects=False)
# r.encoding='utf-8'
# print('网页编码是',r.encoding) #打印默认值，如果人为定义了则打印的是你设
# print('请求的 url 是',r.url)
# print('响应头',r.headers)
# print('相应状态码',r.status_code)
# print('请求历史',r.history)
# print('是否重定向',r.is_redirect)
# # print('二进制内容',r.content)

# session免去设置cookie
# req=requests.session()
# login_url='http://www.xbiquge.la/login.php?jumpurl=http://www.xbiquge.la/'
# r1=req.post(login_url,data={'LoginForm[username]':'zhangke','LoginForm[password]':'123123'})
# r2=req.get('http://www.xbiquge.la/modules/article/bookcase.php')
# r2.encoding='utf-8'
# print(r2.text)

# 图片
# headers = {
#  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
#  }
# url = 'http://www.zgsydw.com/statics/images/linkpic1.jpg'
# res = requests.get(url)
# with open('aa.jpg','wb') as f:
#     f.write(res.content)