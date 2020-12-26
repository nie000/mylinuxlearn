import random

task = list()
res_task = list()


def f():
    # num = random.randint(2,5)
    # y = random.randint(1,4)
    # y_arr = {1:"B",2:"C",3:"D",4:"E"}

    for i in "2345":
        for j in "BCDE":
            task.append(j + i)

    # y_res = y_arr[y]
    # res = y_res+str(num)
    return task


def gen(task):
    while len(task) > 0:
        index = random.randint(0, len(task) - 1)
        res_task.append(task[index])
        task.remove(task[index])


gen(f())

print(res_task)
