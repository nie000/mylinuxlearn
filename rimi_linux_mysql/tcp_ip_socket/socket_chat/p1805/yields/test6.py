# 无限的计算平均值

# 输入:   1.  5-->5   2.  3 --->8    3. 2--->10  4. 2---->12
# 输出:   1.  5       2.  4          3. 3.333    4. 3
def avg():
    num = 0
    total = 0.0
    avg = 0
    # 无限的循环
    while 1:
        # 接收一个值
            val = yield avg
            if not val:
                return avg,total,num
            val = float(val)
            # 计算次数+1
            num += 1
            total += val
            # 平均数等于总数/计算次数
            avg = total / num


def pipe():
    # av = avg()
    # next(av)
    # val = yield
    # while True:
    #     try:
    #         yield av.send(val)
    #     except StopIteration as e:
    #         return e.value
    x = yield from avg()
    return x

def main():
    pip = pipe()
    next(pip)
    while True:
        val = input('number:')
        try:
            num = pip.send(val)
            print(num)
        except StopIteration as e:
            print(e.value)

main()