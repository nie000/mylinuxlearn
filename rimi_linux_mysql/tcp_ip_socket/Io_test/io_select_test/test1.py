from urllib.parse import urlparse

url = 'http://www.google.com/geta/'
urls = urlparse(url)
host = urls.netloc
path = urls.path

print(host)
print(path)