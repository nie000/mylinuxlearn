import time
import requests

url = 'http://blog.jobbole.com/{}'

start_time = time.time()
for i in range(200):
    data = requests.get(url.format(i+114510))
    print(data)

end_time = time.time()

print('共计耗时{}'.format(end_time-start_time))
