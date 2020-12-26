data = {
    'A班': [90, 89, 60, 68],
    'B班': [90, 13, 43, 13, 53],
    'C班': [12, 86, 43, 34, 89, 98, 89]
}


# 调用方 被调用方 管道

# 被调用方
def avg():
    total = 0
    num = 0
    avg = 0
    while 1:
        # 左边是每次接收过来的值(待计算的值) 每次计算的结果
        val = yield avg
        # 如果没有数据,结束整个计算式
        if not val:
            # 遇到return会抛出stop的错 错误里面带的有return后面的值
            return total, num, avg
        # 每次总分加上新过来值
        total += float(val)
        # 每次平均数的除数+1
        num += 1
        avg = total / num


# 调用方
def pipe():
    # yield from 自带初始化
    res = yield from avg()
    return res


def main(data):
    res = {}
    for k, scores in data.items():
        # glavgobal
        # 每次遍历 k就是 A班|B班 scores -->[12, 86, 43, 34, 89, 98, 89]
        pip = pipe()
        next(pip)
        for score in scores:
            pip.send(score)
        try:
            pip.send(None)
        except StopIteration as e:
            total, num, average = e.value
            res[k] = "总分{},人数{},平均数{}".format(total, num, average)
    return res


m = main(data)

print(m)

# yield from可以作为一个管道,帮我们传递值


# 1. yield from "ab"
# 2. 记住,yield from 可以作为管道
