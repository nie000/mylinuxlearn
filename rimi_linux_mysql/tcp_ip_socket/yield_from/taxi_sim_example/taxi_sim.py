import collections
import queue
import random
Event = collections.namedtuple('Event', 'time proc action')


def taxi_process(ident, trips, start_time=0):
    time = yield Event(start_time, ident, 'leave garage')
    for i in range(trips):
        time = yield Event(time, ident, 'pick up passenger')
        time = yield Event(time, ident, 'drop off passenger')

    yield Event(time, ident, 'going home')


class Simulator:

    def __init__(self,taxis):

        self.events = queue.PriorityQueue()
        self.taxis = taxis.copy()

    def run(self,end_time):
        for _,i in self.taxis.items():
            first_event = next(i)
            self.events.put(first_event)

        sim_time = 0
        while sim_time < end_time:
            if self.events.empty():
                print('end events')
                break
            current_event = self.events.get()
            sim_time,taxi_id,actions = current_event
            print('taxi:',taxi_id,'at:',sim_time,'do',current_event)
            next_time = sim_time + random.randint(1,8)
            try:
                next_event = self.taxis[taxi_id].send(next_time)
            except StopIteration:
                del self.taxis[taxi_id]
            else:
                self.events.put(next_event)
        else:
            print('time out')

def main(taxi_num):
    taxis = dict()
    for i in range(taxi_num):
        #生成出租车的对象,间隔发车,运营次数随机
        taxis[i] = taxi_process(i, random.randint(10,20), start_time=random.randint(0,10))
    sim = Simulator(taxis)
    sim.run(120)



if __name__ == '__main__':
    # taxi = taxi_process(ident=5,trips=2,start_time=7)
    # print((next(taxi)))
    # print(taxi.send(9))
    # print(taxi.send(14))
    # print(taxi.send(24))
    # print(taxi.send(34))
    # print(taxi.send(44))
    # print(taxi.send(54))
    # print(taxi.send(64))
    main(9)
