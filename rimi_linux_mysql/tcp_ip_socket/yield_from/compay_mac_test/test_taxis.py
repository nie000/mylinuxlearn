import collections
import queue
import random

event = collections.namedtuple('event', 'time id action')


# yield 事件
def event_gen(start_time, id, trips):
    time = yield event(start_time, id, 'leave home')
    for i in range(trips):
        time = yield event(time, id, 'pick up')
        time = yield event(time, id, 'drop pass')
    yield event(time, id, 'go home')


class Sim:
    def __init__(self, taxi_num):
        self.events = queue.PriorityQueue()
        self.taxis = []
        self.gen_taxis(taxi_num)
        self.taxis_env_gen = dict()
        for i in self.taxis:
            # 初始化每个出租车的生成器
            self.taxis_env_gen[i] = event_gen(start_time=1, id=i, trips=3)
            # 启动生成器，并且把生成器产出的第一个事件交给任务队列
            self.events.put(next(self.taxis_env_gen[i]))

    def gen_taxis(self, num):
        # 初始化出租车对象
        for i in range(num):
            self.taxis.append(i)

    def run(self):
        while True:
            # 取出最靠前的事件
            env = self.events.get()
            time, id, action = env
            print(env)
            try:
                env_gener = self.taxis_env_gen[id]
                self.events.put(env_gener.send(time + random.randint(2, 5)))
            except StopIteration:
                print('taxi:{} tasks end'.format(id))
                del(self.taxis_env_gen[id])


sim = Sim(3)
sim.run()
