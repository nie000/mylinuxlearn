# 1. 出租车随机事件
# 2. 出发 载客 下客 回家
from collections import namedtuple
from random import randint
# 优先队列
from queue import PriorityQueue, Queue

Event = namedtuple('Event', 'time id event')


class Sim:

    def __init__(self, n=3):
        self.taxis = []
        # 生成出租车
        self.gen_taxis(n)
        # 自动的排序 权重越小越先被取出来
        self.queue = PriorityQueue()
        self.gen()
        # 按照tuple的第一个值来作为权重
        # self.queue.put(Event(1,1,'出发'))

    def gen_taxis(self, n=1):
        for i in range(n):
            taxi = self.event_gen(trips=randint(10, 20), start_time=randint(1, 10), taxi_id=i + 1)
            self.taxis.append(taxi)

    # 生成器
    def event_gen(self, trips=10, start_time=0, taxi_id=1):
        """
        trips表示的是出租车载客下客多少次
        :param n:
        :return:
        """
        # 新加了出租车编号和事件发生的时间点
        time = yield Event(start_time, taxi_id, '出发')
        for i in range(trips):
            time = yield Event(time, taxi_id, '载客')
            time = yield Event(time, taxi_id, '下客')
        yield Event(time, taxi_id, '回家')

    # 主循环 驱动事件
    def loop(self):
        """
        按照时间的大小来排序 主循环程序不断的去激活事件,停止事件,事件多久激活,都是主循环来决定的
        :return:
        """
        # 不断执行时间
        while 1:
            # 第一次循环 肯定是某一个出租车出发
            event = self.queue.get()
            # 拆包event
            time, taxi_id, event_name = event
            self.echo_event(time, taxi_id, event_name)
            # 生成下一个事件
            # taxi_id-1=i
            try:
                """
                执行方 --->loop --->send 
                执行方 --->event_gen ---> yield
                执行方 --->loop 
                #暂停 --->  协程
                loop --> event_gen --> loop --> event_gen
                """
                event = self.taxis[taxi_id - 1].send(time + randint(1, 10))
                """
                """
                self.queue.put(event)
            except StopIteration:
                print('出租车{}完成了任务'.format(taxi_id))

            # 第一次: queue里面有三个值{分组 出租1在1出发 出租2在5分发 出租3在4分钟出场}某个出租在1分钟出发,event=出租出发，下一个事件可能是 第2分钟 出租载客

    def gen(self):
        # 激活taxis
        for taxi in self.taxis:
            event = next(taxi)
            self.queue.put(event)

    def echo_event(self, time, taxi_id, event):
        print('{}号出租车 在{}分钟 发生{}事件'.format(taxi_id, time, event))


s = Sim()
s.loop()
