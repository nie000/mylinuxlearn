# def bubble_sort(l):
#     length = len(l)
#     for i in range(length):
#         try:
#             for j in range(length-i):
#                 if l[j] > l[j+1]:
#                     tmp = l[j+1]
#                     l[j+1] = l[j]
#                     l[j] = tmp
#         except IndexError:
#             pass
#
#     return l

#变量其实是地址 # 101011100111101011 #逻辑地址  -->物理地址 01111110001100
import datetime

def get_time():
    return datetime.time()

def f2():
    now = get_time()

def select_sort(l):

    now = get_time()

    length = len(l)
    for i in range(length):
        little = l[i]
        min_index = i+1
        for j in range(i+1,length):
            if l[j] < l[min_index]:
                min_index = j
        try:
            if l[min_index] < little:
                tmp = little
                l[i] = l[min_index]
                l[min_index] = tmp
        except IndexError:
            pass

    return l







a1 = [1,2,10,3,4,5,9,56,6,7,134,9]

# print(select_sort(a1))


def muti_seli():
    sql = 'select 1;'
    sql2 = 'select 2;'


x = None
x12 = 'None'


str1 = "\\r"

print(str1)

print('-------')