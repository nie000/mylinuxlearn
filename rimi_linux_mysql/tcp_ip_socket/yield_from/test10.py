def count():
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
    return avg


def pipe(res, k):
    while 1:
        r = yield from count()
        res[k] = r


def start(data):
    res = {}
    for k, v in data.items():
        group = pipe(res, k)
        next(group)
        for v1 in v:
            group.send(v1)
        group.send(None)
    print(res)


data = {
    'A班': [90, 89, 60, 68],
    'B班': [90, 13, 43, 13, 53],
    'C班': [12, 86, 43, 34, 89, 98, 89]
}
start(data)
