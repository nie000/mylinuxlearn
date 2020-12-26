# 出租车仿真程序
# 模仿出租车(多辆)在 120分钟之内的随机活动情况
# 事件驱动, 从家里面出发,载客-->下客,循环(80), 回家睡觉
# 做仿真事件, 给出租车一个随机的时间  在n分钟之后出发,在n分钟之后载客,在n分钟之后下客(循环),再n分钟之后回家

# 多辆  A B C

# A在1分钟出发 B在5分钟出发  A在6分钟载客 C在7分钟出发  A在10分钟下客 B在11分钟载客

from collections import namedtuple  # 有tuple的性质,又有 dict的性质 还有object的性质
import random
import queue

# 第一个参数必须和变量一样 出租车事件, time是表示出租车在xx分钟干什么事情, id表示哪一辆出租车, event 表示事件
# 有出发 载客 下客 回家
Event = namedtuple('Event', 'time id event')

# t1 = taxi_event(1, start_time=5, trips=50)
#
# t,id,event = next(t1)
#
# echo(t,id,event)
#
# for i in range(10):
#     next_time = t+random.randint(1,5)
#     t,id,event = t1.send(next_time)
#     echo(t,id,event)


class Simulator:

    def __init__(self, taxi_num=3):
        """
        出租车的数量
        """
        self.taxis_events = queue.PriorityQueue()
        self.taxis = []
        for i in range(taxi_num):
            """
            开始的时间随机
            """
            taxi_id = i + 1  # 出租编号
            start_time = random.randint(1, 20)
            trips = random.randint(10, 20)
            #生成器对象
            tmp_taxi = self.taxi_event(start_time=start_time, id=taxi_id, trips=trips)
            self.taxis.append(tmp_taxi)

    # taxi代表出租车的事件循环
    def taxi_event(self, start_time=0, id=1, trips=50):
        #(5,1,'离开家') (1,2,'离开家')
        time = yield Event(start_time, id, '离开家')
        # 出租车载客是有次数
        for i in range(trips):
            # 主程序会把下一个事件的时间传递过来 一定会传递 > 5
            time = yield Event(time, id, '载客')
            time = yield Event(time, id, '下客')
        yield Event(time, id, '回家')

    def run(self):
        """
        离开家
        :return:
        """
        #把每个出租车激活,并且把离开家的事件加入到任务队列去
        for i in self.taxis:
            event = next(i)
            self.taxis_events.put(event)

        while True:
            #event就是tuple
            if self.taxis_events.qsize() == 0:
                break
            event = self.taxis_events.get()
            t,taxi_id,event_name = event
            self.echo(t,taxi_id,event_name)
            next_time = t+random.randint(1,10)
            #生成出下一个事件
            try:
                event = self.taxis[(taxi_id-1)].send(next_time)
            except StopIteration:
                continue
            #把下一个事件丢给queue 排定时间
            self.taxis_events.put(event)
        print('事件已经全部结束')


    def echo(self,t, id, event):
        print('出租车号:{} 在第{}分钟{}'.format(id, t, event))


if __name__ == "__main__":
    s = Simulator()
    s.run()