import requests
import time
import threading
#url = "http://blog.jobbole.com/114261/"

def get_html(url):
    res = requests.get(url)
    print(url)

start_time = time.time()
url = "http://blog.jobbole.com/"
thread_list = []
for i in range(10,90):
    tmp_url = "http://blog.jobbole.com/1142"+str(i)+'/'
    tmp_thread = threading.Thread(target=get_html,args=(tmp_url,))
    thread_list.append(tmp_thread)
    # get_html(tmp_url)

for i in thread_list:
    i.start()

for i in thread_list:
    i.join()

end_time = time.time() - start_time

print(end_time)