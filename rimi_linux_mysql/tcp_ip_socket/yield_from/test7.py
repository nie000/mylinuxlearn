from collections import namedtuple,defaultdict
import random
import queue

Event = namedtuple("Event", "time ident action")


# 不断的去生成事件
def taxi_process(trips, start_time, ident):
    # 第一件事永远是 离开 ident出租车编号
    time = yield Event(start_time, ident, 'leave home')
    for i in range(trips):
        time = yield Event(time, ident, 'pick up pass')
        time = yield Event(time, ident, 'drop up pass')
    yield Event(time, ident, 'go home')


def main(taxi_num):
    taxis = dict()
    # tasks  pickup 5  drop 0
    events = queue.PriorityQueue()
    for i in range(taxi_num):
        tmp_start_time = random.randint(0, 5)
        tmp_tasks = random.randint(2, 8)
        taxi = taxi_process(tmp_tasks, tmp_start_time, i)
        taxis[i] = taxi
        event = next(taxi)
        events.put(event)

    while True:
        event = events.get()
        time, ident, action = event
        print_msg(time, ident, action)
        next_time = time + random.randint(2, 10)
        taxi = taxis[ident]
        try:
            event = taxi.send(next_time)
            events.put(event)
        except Exception:
            print('task {} finish task'.format(ident))


def print_msg(time, ident, action):
    print('time:{} taxi_num:{} action {}'.format(time, ident, action))

main(8)
