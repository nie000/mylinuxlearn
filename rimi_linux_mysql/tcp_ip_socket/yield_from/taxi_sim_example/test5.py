import collections
import random
import queue
event = collections.namedtuple('event', 'time id action')


def events(start_time, id, trip_num):
    time = yield event(start_time, id, 'leave home')
    for i in range(trip_num):
        time = yield event(time, id, 'pick up')
        time = yield event(time, id, 'drop')

    yield event(id, time, 'go home')

class Sim:
    def __init__(self,taxi_num):
        self.events = queue.PriorityQueue()
        self.taxi_dict = dict()
        for i in range(taxi_num):
            self.taxi_dict[i] = events(random.randint(1,5),i,random.randint(10,20))
            x = next(self.taxi_dict[i])
            print(x)
            self.events.put(x)

    def run(self):

        while True:
            evn = self.events.get()
            tmp_time,tmp_id,tmp_action = evn
            try:
                next_time = tmp_time+random.randint(2,4)
                next_env = self.taxi_dict[tmp_id].send(next_time)
            except StopIteration:
                print('end')
            else:
                self.events.put(next_env)
                print(next_env)

sim = Sim(5)
sim.run()