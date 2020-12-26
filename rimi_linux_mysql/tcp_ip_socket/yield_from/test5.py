def count():
    print('新的count----')
    total = 0.0
    avg = 0.0
    num = 0
    while True:
        data = yield avg
        if not data:
            break
        total += data
        num += 1
        avg = total / num
        print(avg)
    print('完成count')
    return num, avg


def start(data):
    res = {}
    for k, v in data.items():
        # print(k,v)
        group = count()
        next(group)
        for v1 in v:
            group.send(v1)
        try:
            group.send(None)
        except StopIteration as e:
            res[k] = e.value
    print(res)


data = {
    'A班': [90, 89, 60, 68],
    'B班': [90, 13, 43, 13, 53],
    'C班': [12, 86, 43, 34, 89, 98, 89]
}

start(data)

