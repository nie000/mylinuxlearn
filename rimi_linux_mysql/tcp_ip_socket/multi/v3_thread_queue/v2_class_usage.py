import threading
import time


class TestThread(threading.Thread):
    def __init__(self, target=None, args=None):
        # 调用父类方法
        super().__init__()
        self.target = target
        self.args = args

    # 当调用函数的时候使用的方法
    def run(self):
        self.target(*self.args)


def test(i):
    time.sleep(i)
    print('execute thread:{}'.format(i))


def loop():
    my_tasks = []
    for i in range(5):
        my_tasks.append(TestThread(target=test, args=(i,)))
    for i in my_tasks:
        i.start()
    for i in my_tasks:
        i.join()
    print("all down")

if __name__ == "__main__":
    loop()
