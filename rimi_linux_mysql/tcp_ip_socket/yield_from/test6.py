import collections
import queue
import random

Event = collections.namedtuple('Event', 'time ident action')


def taxi_process(ident, trips, start_time=0):
    time = yield Event(start_time, ident, 'leave home')
    for i in range(trips):
        time = yield Event(time, ident, 'pick up passenger')
        time = yield Event(time, ident, 'drop passenger')

    yield Event(time, ident, 'go home')


class Sim:
    def __init__(self, taxi_num):
        self.tasks = queue.PriorityQueue()
        self.taxi_num = taxi_num
        self.taxis = list()
        self.gen_taxis()

    def gen_taxis(self):
        for i in range(self.taxi_num):
            tmp = taxi_process(i, random.randint(5, 10), random.randint(0, 4))
            tmp_evn = next(tmp)
            self.tasks.put(tmp_evn)
            self.taxis.append(tmp)

    def run(self):
        while True:
            if self.tasks.empty():
                print('all over---')
                break
            tmp_evn = self.tasks.get()
            time, ident, action = tmp_evn
            print('taxi:{}--{}--at {}minute '.format(ident, action, time))
            next_time = int(time) + random.randint(2, 20)
            taxi = self.taxis[ident]
            try:
                next_evn = taxi.send(next_time)
            except StopIteration:
                print('taxi {} finish tasks'.format(ident))
                # del(self.taxis[ident])
            else:
                self.tasks.put(next_evn)


sim = Sim(3)
sim.run()
