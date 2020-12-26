from urllib import parse
url = "https://gitee.com"
url_dict = parse.urlparse(url)

host = url_dict.hostname
path = url_dict.path
if len(path) == 0:
    path = "/"

pass